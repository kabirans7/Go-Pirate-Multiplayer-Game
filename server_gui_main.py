import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from chatbot.bot_engine import PirateEaseBot
from chatbot.bot_backend import escalate_to_human
from battle.character_factory import CharacterFactory
from battle.battle_manager import BattleManager
from main.db_manager import DBManager

class GameServerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("GoPirates Server")
        self.chat_display = scrolledtext.ScrolledText(self.window, state='disabled', width=80, height=25)
        self.chat_display.pack(padx=10, pady=10)

    def log(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def start(self):
        self.window.mainloop()

    def close(self):
        self.window.destroy()

class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.clients = []
        self.client_names = {}
        self.characters = {}
        self.battle_manager = None
        self.db = DBManager.get_instance()
        self.bot = PirateEaseBot()
        self.gui = GameServerGUI()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((host, port))
            self.server.listen()
            print(f"[SERVER] Listening on {host}:{port}")
        except Exception as e:
            print(f"[SERVER ERROR] Failed to bind/listen: {e}")
            self.gui.close()
            return

        threading.Thread(target=self.accept_clients, daemon=True).start()

    def log_gui(self, msg):
        self.gui.log(msg)

    def broadcast(self, msg, sender=None):
        for client in self.clients:
            if client != sender:
                try:
                    client.send(msg.encode())
                except:
                    client.close()
                    if client in self.clients:
                        self.clients.remove(client)

    def handle_client(self, client):
        try:
            client.send("Enter your name: ".encode())
            intro = client.recv(1024).decode().strip()

            if "|" not in intro:
                client.send("Invalid intro format. Disconnecting.\n".encode())
                return

            name, char_type = intro.split("|")
            role = char_type.strip().lower()

            self.client_names[client] = name
            character = CharacterFactory.create_character(name, char_type)
            self.characters[client] = character

            self.clients.append(client)
            client.send("OK".encode())
            self.log_gui(f"[CONNECTED] {name} joined as {char_type}")
            self.broadcast(f"{name} has joined the battle as {char_type}!", client)

            if len(self.clients) == 3:
                self.start_battle()

            while True:
                msg = client.recv(1024).decode().strip()
                if not msg:
                    continue

                if msg.startswith("/bot"):
                    question = msg[4:].strip()
                    if not question:
                        client.send("Ask the bot something after /bot, like '/bot how do I attack?'\n".encode())
                        continue

                    answer = self.bot.respond(question)
                    client.send(f"Bot: {answer}".encode())

                    if "I don't understand" in answer:
                        self.db.log_unknown(name, question)
                    else:
                        self.db.log_bot(name, question, answer)

                    self.log_gui(f"[BOT][{name}] Q: {question} → A: {answer}")

                elif self.battle_manager and msg.startswith("/"):
                    self.battle_manager.handle_action(client, msg)

                else:
                    self.db.log_chat(name, msg)
                    self.log_gui(f"[CHAT][{name}] {msg}")
                    self.broadcast(f"{name}: {msg}", client)

        except Exception as e:
            print(f"[SERVER] Error with client: {e}")
            self.cleanup_client(client)


    def start_battle(self):
        self.log_gui("[BATTLE] All players joined. Starting battle...")
        self.broadcast("[BATTLE STARTED] Prepare for combat!")
        self.battle_manager = BattleManager(self.clients, self.characters, self)

    def cleanup_client(self, client):
        name = self.client_names.get(client, "Unknown")
        if client in self.clients:
            self.clients.remove(client)
        if client in self.client_names:
            del self.client_names[client]
        if client in self.characters:
            del self.characters[client]
        self.broadcast(f"{name} has left the game.")
        self.log_gui(f"[DISCONNECTED] {name}")

    def accept_clients(self):
        self.log_gui("[SERVER READY] Waiting for 3 players...")
        while True:
            try:
                client, addr = self.server.accept()
                print(f"[SERVER] Accepted connection from {addr}")
                threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()
            except Exception as e:
                print(f"[SERVER ERROR] Accept failed: {e}")

    def run(self):
        self.gui.start()

if __name__ == "__main__":
    print("[SERVER] Launching GoPirates server GUI...")
    GameServer().run()
