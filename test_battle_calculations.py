import pytest
from battle.character_factory import CharacterFactory
from battle.battle_manager import BattleManager

class Client: 
    def __init__(self, name):
        self.name = name
        self.sent_messages = []

    def send(self, msg):
        self.sent_messages.append(msg.decode() if isinstance(msg, bytes) else msg)

@pytest.fixture
def set_battle():
    valid_types = CharacterFactory.get_character_names()
    assert "Captain" in valid_types and "Gunner" in valid_types and "Medic" in valid_types
    clients = [Client(f"Player{i}") for i in range(1,4)]

    characters = {
        clients[0]: CharacterFactory.create_character("Player1", "Captain"),
        clients[1]: CharacterFactory.create_character("Player2", "Gunner"),
        clients[2]: CharacterFactory.create_character("Player3", "Medic")
    }

    mock_server = type("MockServer", (), {
        "log_gui": lambda self, msg: None,
        "client_names": {clients[0]: "Player1", clients[1]: "Player2", clients[2]: "Player3"},
        "broadcast": lambda self, msg: None
    })()

    battle_manager = BattleManager(clients, characters, mock_server)
    return clients, characters, battle_manager

def test_attack_reduces_health(set_battle):
    clients, characters, bm = set_battle
    attacker = clients[0]
    target = clients[1]

    init_hp = characters[target].hp
    bm.handle_action(attacker, "/attack Player2")
    assert characters[target].hp < init_hp

def test_defend_reduces_incoming_damage(set_battle):
    clients, characters, bm = set_battle
    defender = clients[1]
    attacker = clients[0]

    bm.handle_action(defender, "/defend")
    init_hp = characters[defender].hp
    bm.handle_action(attacker, "/attack Player2")
    assert characters[defender].hp > init_hp - 20
    assert not characters[defender].is_defending


def test_turn_rotation(set_battle):
    clients, characters, bm = set_battle
    start_index = bm.turn_index
    current = bm.turn_order[start_index]
    bm.handle_action(current, "/defend")
    assert bm.turn_index != start_index