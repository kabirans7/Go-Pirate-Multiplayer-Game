from main.db_manager import DBManager
from .bot_query_handlers import QuestionHandler
from .bot_backend import escalate_to_human
from .bot_utils import clean_text

class PirateEaseBot:
    def __init__(self):
        self.handler = QuestionHandler()

    def respond(self, user_input):
        db = DBManager()  # Create DBManager instance
        user_input = clean_text(user_input)
        answer = self.handler.get_answer(user_input)

        if answer:
            db.log_bot("Player", user_input, answer)  # Replace "Player" with actual player name if needed
            return answer
        else:
            db.log_unknown("Player", user_input)
            return escalate_to_human(user_input)
