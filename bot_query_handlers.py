from .bot_utils import clean_text

class QuestionHandler:
    def __init__(self):
        self.responses = {
            "attack": "Use /attack <name> during your turn to strike an enemy.",
            "defend": "Use /defend to reduce incoming damage until your next turn.",
            "special": "Special moves are powerful actions. Use /special <name> (or yourself if Medic).",
            "poison": "Poison deals 2 damage per turn for 2 turns. It can stack with other damage.",
            "stun": "Stunned players skip their next turn and can't act.",
            "shield": "Defending gives you a temporary shield that cuts damage in half.",
            "heal": "The Medic's special heals for 10 HP and grants a shield.",
            "help": (
                "Try asking things like:\n"
                "- how do I attack?\n"
                "- what does defend do?\n"
                "- what is a special move?\n"
                "- what does poison mean?\n"
                "- what happens when stunned?"
            )
        }

    def get_answer(self, question):
        question = clean_text(question)
        for keyword, answer in self.responses.items():
            if keyword in question:
                return answer
        return None  # Triggers escalation in bot_engine
