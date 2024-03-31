import random


def check_balance(db: dict, amount: int) -> bool:
    if db['balance'] >= amount:
        return True
    else:
        return False


def check_position(db: dict, position: str) -> bool:
    for i in db.keys():
        if db[i]['type'] == "FACTORY":
            if "warehouse" not in db[i].keys():
                return False
            else:
                if position in db[i]["warehouse"].keys() and db[i]["warehouse"][position] != 0:
                    return True
                else:
                    return False


def check_not_full(db: dict) -> bool:
    for i in db.keys():
        if db[i]['type'] == "FACTORY":
            if "warehouse" not in db[i].keys():
                return True
            else:
                if sum(db[i]["warehouse"].values()) < 3:
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
