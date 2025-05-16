import sqlite3
from datetime import datetime
import os

class DBManager:
    _instance = None

    def __init__(self):
        db_path = os.path.join("data", "game_chat.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._setup()

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = DBManager()
        return cls._instance

    def _setup(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chat_logs (
                                player TEXT, message TEXT, timestamp TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chatbot_logs (
                                player TEXT, question TEXT, answer TEXT, timestamp TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS unknown_queries (
                                player TEXT, question TEXT, timestamp TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TurnLog (
                                player TEXT, action TEXT, target TEXT, result TEXT, timestamp TEXT)''')
        self.conn.commit()

    def log_chat(self, player, message):
        self.cursor.execute("INSERT INTO chat_logs VALUES (?, ?, ?)",
                            (player, message, datetime.now().isoformat()))
        self.conn.commit()

    def log_bot(self, player, question, answer):
        self.cursor.execute("INSERT INTO chatbot_logs VALUES (?, ?, ?, ?)",
                            (player, question, answer, datetime.now().isoformat()))
        self.conn.commit()

    def log_unknown(self, player, question):
        self.cursor.execute("INSERT INTO unknown_queries VALUES (?, ?, ?)",
                            (player, question, datetime.now().isoformat()))
        self.conn.commit()

    def log_turn(self, player, action, target, result):
        self.cursor.execute("INSERT INTO TurnLog VALUES (?, ?, ?, ?, ?)",
                            (player, action, target, result, datetime.now().isoformat()))
        self.conn.commit()
