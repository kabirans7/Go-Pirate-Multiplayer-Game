def perform_attack(attacker, target):
    if attacker.name == target.name:
        return f"{attacker.name} cannot attack themselves!"

    damage = attacker.attack
    if getattr(target, "is_defending", False):
        damage = max(1, damage // 2)

    target.hp -= damage
    return f"{target.name} takes {damage} damage. Remaining HP: {target.hp}"


def perform_defend(player):
    player.is_defending = True
    return f"{player.name} is defending and will take reduced damage next turn."


def perform_special(attacker, target):
    if attacker.role == "captain":
        target.stunned = True
        result = f"{attacker.name} stuns {target.name} for 1 turn!"
    elif attacker.role == "gunner":
        target.poison_turns = 2
        result = f"{attacker.name} poisons {target.name} for 2 turns!"
    elif attacker.role == "medic":
        heal_amt = 8
        attacker.hp = min(attacker.hp + heal_amt, attacker.max_hp)
        attacker.defending = True
        result = f"{attacker.name} heals for {heal_amt} HP and defends!"
    else:
        result = f"{attacker.name} uses a mysterious special move..."

    return result


def apply_status_effects(characters):
    logs = []
    for char in characters.values():
        if getattr(char, "poisoned", 0) > 0:
            char.hp -= 2
            char.poisoned -= 1
            logs.append(f"{char.name} takes 2 poison damage. Remaining HP: {char.hp}")
    return logs


def clear_statuses(character):
    character.is_defending = False
    if not character.stunned:
        character.stunned = False
