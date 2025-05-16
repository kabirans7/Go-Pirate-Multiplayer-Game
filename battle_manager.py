from main.db_manager import DBManager
from battle.combat_logic import (
    perform_attack, perform_defend, perform_special,
    apply_status_effects, clear_statuses
)

class BattleManager:
    def __init__(self, sockets, characters, server):
        self.db = DBManager()
        self.server = server
        self.clients = sockets
        self.characters = characters
        self.turn_order = sockets[:]
        self.turn_index = 0
        self.active = True
        self.start_turn()

    def start_turn(self):
        if not self.active:
            return

        poison_logs = apply_status_effects(self.characters)
        for log in poison_logs:
            self.server.broadcast(f"\n{log}\n")

        current = self.turn_order[self.turn_index]
        char = self.characters[current]

        clear_statuses(char)

        if char.stunned:
            name = self.server.client_names[current]
            self.server.broadcast(f"\n{name} is stunned and skips their turn.\n")
            char.stunned = False
            self.advance_turn()
            return

        name = self.server.client_names[current]
        self.server.broadcast(f"\n[TURN] It's {name}'s turn!")
        current.send("\n[Your Turn] Use: /attack <name>, /defend, or /special <name>.\nType /bot for help.\n".encode())

    def check_game_over(self):
        alive = [c for c in self.characters.values() if c.hp > 0]
        if len(alive) == 1:
            winner = alive[0].name
            self.server.broadcast(f"\n{winner} wins the battle! 🏴‍☠️\n")
            self.active = False
            return True
        return False

    def handle_action(self, client, command):
        if not self.active:
            return

        current = self.turn_order[self.turn_index]
        if client != current:
            client.send("[Not your turn] Wait for your turn.\n".encode())
            return

        char = self.characters[client]
        name = self.server.client_names[client]

        if command.startswith("/attack "):
            target_name = command.split("/attack ", 1)[1].strip()
            target = self.get_socket_by_name(target_name)
            if not target or self.characters[target].hp <= 0:
                client.send(f"Invalid target: {target_name}\n".encode())
                return
            result = perform_attack(char, self.characters[target])
            self.server.broadcast(f"\n{name} attacks {target_name}! {result}\n")
            self.db.log_turn(name, 'attack', target_name, result)
            if self.check_game_over():
                return

        elif command == "/defend":
            result = perform_defend(char)
            self.server.broadcast(f"\n{name} defends! {result}\n")
            self.db.log_turn(name, 'defend', name, result)
            if self.check_game_over():
                return

        elif command.startswith("/special "):
            target_name = command.split("/special ", 1)[1].strip()
            if char.role == "medic":
                result = perform_special(char, char)
                self.server.broadcast(f"\n{name} uses SPECIAL! {result}\n")
                self.db.log_turn(name, 'special', name, result)
                if self.check_game_over():
                    return
            else:
                target = self.get_socket_by_name(target_name)
                if not target or self.characters[target].hp <= 0:
                    client.send(f"Invalid special target: {target_name}\n".encode())
                    return
                result = perform_special(char, self.characters[target])
                self.server.broadcast(f"\n{name} uses SPECIAL on {target_name}! {result}\n")
                self.db.log_turn(name, 'special', target_name, result)
                if self.check_game_over():
                    return

        else:
            client.send("Invalid command. Use /attack <name>, /defend, or /special <name>\n".encode())
            return

        apply_status_effects(self.characters)
        self.remove_defeated()
        self.advance_turn()

    def advance_turn(self):
        if not self.active:
            return
        self.turn_index = (self.turn_index + 1) % len(self.turn_order)
        self.start_turn()

    def remove_defeated(self):
        defeated = [sock for sock, char in self.characters.items() if char.hp <= 0]
        for sock in defeated:
            name = self.server.client_names[sock]
            if sock in self.turn_order:
                self.turn_order.remove(sock)
            self.server.broadcast(f"\n{name} has been defeated!\n")

        if len(self.turn_order) == 1:
            winner = self.server.client_names[self.turn_order[0]]
            self.server.broadcast(f"\n{winner} is the last pirate standing! VICTORY!\n")
            self.server.log_gui(f"[VICTORY] {winner} wins!")
            self.end_battle()

    def get_socket_by_name(self, name):
        for sock, pname in self.server.client_names.items():
            if pname.lower() == name.lower():
                return sock
        return None

    def end_battle(self):
        self.active = False
        for sock in self.clients:
            try:
                sock.send("GAME OVER. Thanks for playing.\n".encode())
            except:
                pass
