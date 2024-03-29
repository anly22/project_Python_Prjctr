import random

def check_balance(database: dict, amount: int) -> bool:
    if database['balance'] >= amount:
        return True
    else:
        return False


def check_amount(database: dict) -> int:
    return len(database)


def check_position(database: dict, position: str) -> bool:
    for i in database.keys():
        if database[i]['type'] == "FACTORY":
            if "warehouse" not in database[i].keys():
                return False
            else:
                if position in database[i]["warehouse"].keys() and database[i]["warehouse"][position] != 0:
                    return True
                else:
                    return False


def check_not_full(database: dict[int: dict]):
    for i in database.keys():
        if database[i]['type'] == "FACTORY":
            if "warehouse" not in database[i].keys():
                return True
            else:
                if sum(database[i]["warehouse"].values()) < 3:
                    return True
                else:
                    return False


def get_d_loc(aim: str) -> list:
    d_loc = []
    if aim == 'move':
        while True:
            x = random.randint(-2, 2)
            y = random.randint(-2, 2)
            if (abs(x) + abs(y)) <= 2 and (abs(x) + abs(y)) != 0:
                d_loc = [x, y]
                return d_loc
    elif aim == 'build':
        while True:
            x = random.randint(-5, 5)
            y = random.randint(-5, 5)
            if (abs(x) + abs(y)) <= 5 and (abs(x) + abs(y)) != 0:
                d_loc = [x, y]
                return d_loc
    elif aim == 'deploy':
        d_loc = random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])
        return d_loc
