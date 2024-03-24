def check_balance(database: dict, amount: int):
    if database['balance'] >= amount:
        return True
    else:
        return False


def check_amount(database: dict):
    return len(database)


def check_position(database: list[dict], position: str):
    for i in database.keys():
        if database[i]['type'] == "FACTORY":
            if "warehouse" not in database[i].keys():
                return False
            else:
                if position in database[i]["warehouse"].keys():
                    return True
                else:
                    return False