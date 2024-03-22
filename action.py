def check_round(game_database: dict):
    return game_database['round']


def check_balance(database: dict, amount: int):
    if database['balance'] >= amount:
        return True
    else:
        return False


def check_amount(database: dict):
    return len(database)
