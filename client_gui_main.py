import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
from battle.character_factory import CharacterFactory

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((host, port))
            print("[CLIENT] Connected to server.")
        except Exception as e:
            messagebox.showerror("Connection Failed", f"Unable to connect to server: {e}")
            return

        self.character_name = None
        self.name = None
        self.running = True

        # GUI setup
        self.window = tk.Tk()
        self.window.title("GoPirates - Player")
        self.chat_display = scrolledtext.ScrolledText(self.window, state='disabled', width=70, height=25)
        self.chat_display.pack(padx=10, pady=10)

        self.entry_field = tk.Entry(self.window, width=60)
        self.entry_field.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        self.entry_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

        self.prompt_for_name_and_character()
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.window.protocol("WM_DELETE_WINDOW", self.close_client)
        self.window.mainloop()

    def prompt_for_name_and_character(self):
        self.name = simpledialog.askstring("Name", "Enter your pirate name:", parent=self.window)
        if not self.name:
            self.window.destroy()
            return

        options = CharacterFactory.get_character_names()

        def submit_choice():
            choice = choice_var.get()
            if self.send_intro(self.name, choice):
                self.character_name = choice
                character_selection.destroy()
            else:
                messagebox.showerror("Connection Error", "Could not select character. Please try again.")

        character_selection = tk.Toplevel(self.window)
        character_selection.title("Choose Your Character")
        tk.Label(character_selection, text="Choose a character:").pack(pady=5)
        choice_var = tk.StringVar(value=options[0])

        for opt in options:
            tk.Radiobutton(character_selection, text=opt, variable=choice_var, value=opt).pack(anchor=tk.W)

        tk.Button(character_selection, text="Select", command=submit_choice).pack(pady=10)

    def send_intro(self, name, char_type):
        try:
            self.client.send(f"{name}|{char_type}".encode())
            status = self.client.recv(1024).decode()
            return status == "OK"
        except Exception as e:
            print(f"[ERROR] Failed to send intro: {e}")
            return False

    def send_message(self, event=None):
        msg = self.entry_field.get().strip()
        if msg:
            try:
                self.client.send(msg.encode())
                self.entry_field.delete(0, tk.END)
            except Exception as e:
                self.log(f"[SEND ERROR] {e}")
                self.close_client()

    def receive_messages(self):
        while self.running:
            try:
                msg = self.client.recv(1024).decode()
                if not msg:
                    break
                self.log(msg)
            except:
                self.log("[DISCONNECTED] Server closed the connection.")
                self.running = False
                break
        self.client.close()

    def log(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

    def close_client(self):
        self.running = False
        try:
            self.client.close()
        except:
            pass
        self.window.destroy()

if __name__ == "__main__":
    ChatClient()
