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
                return action
            else:
                action = None 
                return action       
        else:
            action = None
            return action
      
