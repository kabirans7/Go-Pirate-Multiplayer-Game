# Base Character Class
class Character:
    def __init__(self, name, hp=100, attack=10):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack

        # Status flags
        self.is_defending = False
        self.stunned = False
        self.poisoned = False
