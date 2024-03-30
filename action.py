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


def check_not_full(database: dict[int: dict]) -> bool:
    for i in database.keys():
        if database[i]['type'] == "FACTORY":
            if "warehouse" not in database[i].keys():
                return True
            else:
                if sum(database[i]["warehouse"].values()) < 3:
                    return True
                else:
                    return False


def get_d_loc(aim: str) -> list[int, int]:
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


def check_not_full_n(database: dict[int: dict], num: int) -> bool:
    for i in database.keys():
        if database[i]['type'] == "FACTORY":
            if "warehouse" not in database[i].keys():
                return True
            else:
                if sum(database[i]["warehouse"].values()) < num:
                    return True
                else:
                    return False


def check_map_near_loc(maparrey: list[list], location: list[int], aim: str) -> list[int, int]:
    x, y = location
    if all(num in range(len(maparrey)) for num in ((x-1), (x+1), (y-1), (y+1))):
        if maparrey[x-1][y] is not None:
            if maparrey[x-1][y]['type'] == aim and maparrey[x-1][y]['agent'] is None:
                return [-1, 0]
            else:
                return get_d_loc('deploy')
        elif maparrey[x][y-1] is not None:
            if maparrey[x][y-1]['type'] == aim and maparrey[x][y-1]['agent'] is None:
                return [0, -1]
            else:
                return get_d_loc('deploy')
        elif maparrey[x+1][y] is not None:
            if maparrey[x+1][y]['type'] == aim and maparrey[x+1][y]['agent'] is None:
                return [1, 0]
            else:
                return get_d_loc('deploy')
        elif maparrey[x][y+1] is not None:
            if maparrey[x][y+1]['type'] == aim and maparrey[x][y+1]['agent'] is None:
                return [0, 1]
            else:
                return get_d_loc('deploy')
        else:
            return get_d_loc('deploy')
    else:
        return get_d_loc('deploy')


def get_loc(database: dict, name: str) -> list[int, int]:
    for i in database.keys():
        if database[i]['type'] == name:
            return database[i]['location']


def check_map_near_bool(maparrey: list[list], location: list[int], aim: str) -> bool:
    x, y = location
    if all(num in range(len(maparrey)) for num in ((x-1), (x+1), (y-1), (y+1))):
        if maparrey[x-1][y] is not None and maparrey[x-1][y]['type'] == aim:
            return True
        elif maparrey[x][y-1] is not None and maparrey[x][y-1]['type'] == aim:
            return True
        elif maparrey[x+1][y] is not None and maparrey[x+1][y]['type'] == aim:
            return True
        elif maparrey[x][y+1] is not None and maparrey[x][y+1]['type'] == aim:
            return True
        else:
            return False
    else:
        return False
