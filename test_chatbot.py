# final_pirate/test_chatbot.py

import pytest
from chatbot.bot_engine import PirateEaseBot

@pytest.fixture
def bot():
    return PirateEaseBot()

def test_known_query_response(bot):
    query = "What does my special move do?"
    response = bot.respond(query)
    assert isinstance(response, str)
    assert response != "I'm not sure about that one yet — a human representative will follow up shortly."
    assert len(response) > 0

def test_unknown_query_triggers_escalation(bot):
    query = "How do I change my weapon?"
    response = bot.respond(query)
    expected = "I'm not sure about that one yet — a human representative will follow up shortly."
    assert response == expected

def test_synonym_handling(bot):
    queries = [
        "Explain my special attack",
        "What is my ultimate move?",
        "Tell me about my finisher move"
    ]
    for query in queries:
        response = bot.respond(query)
        assert isinstance(response, str)

def test_question_handler_loaded(bot):
    assert hasattr(bot, 'handler')
    assert bot.handler is not None

def test_fallback_records_unknown_query(bot):
    query = "What's the weather today?"
    response = bot.respond(query)
    expected = "I'm not sure about that one yet — a human representative will follow up shortly."
    assert response == expected
