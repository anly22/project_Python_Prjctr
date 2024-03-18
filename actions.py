import storage as s


def define_action(id):
    action = None
    for agent in s.agents:
        if id == agent['id'] and agent['type'] == "FACTORY":
            if s.game_database['round'] == 1:
                action = {
                    "type": "BUILD_BOT",
                    "params": {
                    "d_loc": [-1, 2]
                    }
                }
            elif s.game_database['round'] == 2 and s.game_database['balance'] >= 150:
                action = {
                    "type": "ASSEMBLE_POWER_PLANT",
                    "params": {
                        "power_type": "SOLAR_PANELS"
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
            elif s.game_database['round'] == 3:
                # TODO checkout of warehouse:
                action = {
                    "type": "DEPLOY",
                    "params": {
                        "power_type": "SOLAR_PANELS",
                        "d_loc": [-1, 0]
                    }
                    }
            else:
                action = None

#TODO
# action = {
#   "type": "EXPLORE",
#   "params": {}
# }

    return action
