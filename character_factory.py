from battle.character_base import Character

class CharacterFactory:
    @staticmethod
    def get_character_names():
        return ["Captain", "Gunner", "Medic"]

    @staticmethod
    def create_character(name, type_):
        type_ = type_.lower()

        if type_ == "captain":
            char = Character(name, hp=110, attack=12)
            char.role = "captain"
        elif type_ == "gunner":
            char = Character(name, hp=90, attack=16)
            char.role = "gunner"
        elif type_ == "medic":
            char = Character(name, hp=100, attack=9)
            char.role = "medic"
        else:
            char = Character(name)
            char.role = "unknown"

        # Default status setup
        char.is_defending = False
        char.stunned = False
        char.poisoned = 0

        return char
