import storage as s


def define_action(id):
    action = None
    for agent in s.agents:
        if id == agent['id'] and agent['type'] == "FACTORY":
            if s.game_database['round'] == 0:
                action = {
                    "type": "BUILD_BOT",
                    "params": {
                    "d_loc": [-1, 3]
                    }
                }
            else:
                action = None
        
        elif id == agent['id'] and agent['type'] == "ENGINEER_BOT":
            if s.game_database['round'] == 2:
                action = {
                    "type": "MOVE",
                    "params": {
                        "d_loc": [-1, 1]
                    }
                }
            else:
                action = None
        else:
            action = None
        return action
