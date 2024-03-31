import random


def check_balance(db: dict, amount: int) -> bool:
    if db['balance'] >= amount:
        return True
    else:
        return False


# def check_amount(db: dict) -> int:
#     return len(db)


def check_plant(db: dict, plant: str) -> bool:
    for i in db.keys():
        if db[i]['type'] == "FACTORY":
            if "warehouse" not in db[i].keys():
                return False
            else:
                if plant in db[i]["warehouse"].keys() and db[i]["warehouse"][plant] != 0:
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


def get_d_loc(aim: str) -> list[int]:
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


def check_not_full_n(db: dict, num: int) -> bool:
    for i in db.keys():
        if db[i]['type'] == "FACTORY":
            if "warehouse" not in db[i].keys():
                return True
            else:
                if sum(db[i]["warehouse"].values()) < num:
                    return True
                else:
                    return False


def check_near_loc(maparrey: list[list], location: list[int], aim: str) -> list[int]:
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


def get_loc(db: dict, name: str) -> list[int]:
    for i in db.keys():
        if db[i]['type'] == name:
            return db[i]['location']


def check_near(maparrey: list[list], location: list[int], aim: str) -> bool:
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
