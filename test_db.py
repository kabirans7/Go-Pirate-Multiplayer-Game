import pytest
import sqlite3
from main.db_manager import DBManager

class TempDBManager(DBManager):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._setup()

    def _setup(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chat_logs (
                            player TEXT, message TEXT, timestamp TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chatbot_logs (
                            player TEXT, question TEXT, answer TEXT, timestamp TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS unknown_queries (
                            player TEXT, question TEXT, timestamp TEXT)''')
        self.conn.commit()

@pytest.fixture
def db_instance(tmp_path):
    db_path = tmp_path / "test_game_chat.db"
    return TempDBManager(str(db_path))

def test_log_chat(db_instance):
    db_instance.log_chat("TestPlayer", "Hello World!")
    result = db_instance.cursor.execute("SELECT * FROM chat_logs WHERE player=?", ("TestPlayer",)).fetchone()
    assert result is not None
    assert result[0] == "TestPlayer"
    assert result[1] == "Hello World!"

def test_log_bot(db_instance):
    db_instance.log_bot("TestPlayer", "What is my move?", "You can attack or defend.")
    result = db_instance.cursor.execute("SELECT * FROM chatbot_logs WHERE player=?", ("TestPlayer",)).fetchone()
    assert result is not None
    assert result[0] == "TestPlayer"
    assert result[1] == "What is my move?"
    assert result[2] == "You can attack or defend."

def test_log_unknown(db_instance):
    db_instance.log_unknown("TestPlayer", "What is the airspeed of an unladen swallow?")
    result = db_instance.cursor.execute("SELECT * from unknown_queries WHERE player=?", ("TestPlayer",)).fetchone()
    assert result is not None
    assert result[0] == "TestPlayer"
    assert result[1] == "What is the airspeed of an unladen swallow?"

def test_log_chat_multiple_entries(db_instance):
    db_instance.log_chat("UserA", "Hi")
    db_instance.log_chat("UserB", "Hello")
    count = db_instance.cursor.execute("SELECT COUNT(*) FROM chat_logs").fetchone()[0]
    assert count ==2

def test_log_bot_multiple_responses(db_instance):
    db_instance.log_bot("UserA", "Q1", "A1")
    count = db_instance.cursor.execute("SELECT COUNT(*) FROM chatbot_logs").fetchone()[0]
    assert count == 1

def test_log_unknown_duplicate(db_instance):
    db_instance.log_unknown("UserA", "Huh?")
    db_instance.log_unknown("UserA", "Huh?")
    count = db_instance.cursor.execute("SELECT COUNT(*) FROM unknown_queries WHERE player='UserA'").fetchone()[0]
    assert count == 2


    