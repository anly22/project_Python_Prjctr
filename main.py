from flask import Flask, Response, jsonify, request
import json
import random
import action as a


app = Flask(__name__)

game_DB = {
    'balance': None,
    'map_size': None,
    'team': None,
    'round': 0
    }

agents = {}

map = None


@app.route('/health')
def getHealth():
    return Response(status=200)


@app.route('/init', methods=['POST'])
def toInit():
    if request.is_json:
        r = request.get_json()
        game_DB['map_size'] = r['map_size']
        game_DB['balance'] = r['init_balance']
        game_DB['team'] = r['team']
        size = r['map_size']
        map = [[None] * size for _ in range(size)]
        print(map)

        global agents
        agents = {}
        
        return Response(status=200)
    else:
        return Response(status=404)
        

@app.route('/round', methods=['POST'])
def toRound():
    if request.is_json:
        r = request.get_json()
        game_DB['balance'] = r['balance']
        game_DB['round'] = r['round']
        return Response(status=200)
    else:
        return Response(status=404)
   

@app.route('/agent/<int:id>', methods=['POST'])
def toInitAgent(id: int):
    if request.is_json:
        r = request.get_json()
        agents[id] = r
        x, y = r['location']
        map[x][y] = {'agent': {'id': agents[id]['id'], 'type': agents[id]['type']}}
        return Response(status=200)
    else:
        return Response(status=404)


@app.route('/agent/<int:id>', methods=['PATCH'])
def toUpdateAgent(id: int):
    if request.is_json:
        r = request.get_json()
        agents[id].update(r)
        x, y = r['location']
        map[x][y] = {'agent': {'id': agents[id]['id'], 'type': agents[id]['type']}}
        return Response(status=200)
    else:
        return Response(status=404)


@app.route('/agent/<int:id>/action', methods=['GET'])
def toGetAction(id: int):
    agent = agents[id]
    if agent['type'] == "FACTORY":
        if game_DB['round'] == 0: 
            return jsonify({
                "type": "BUILD_BOT",
                "params": {
                "d_loc": [(random.choice([-2, 2]),random.choice([-2, 2]))]
                }
                })
        else:
            if a.check_balance(game_DB, 200) and sum(agent["warehouse"].values()) < 2:
                return jsonify({
                    "type": "ASSEMBLE_POWER_PLANT",
                    "params": {
                    "power_type": "WINDMILL"
                    }
                    })
            elif a.check_balance(game_DB, 600):
                return jsonify({
                    "type": "BUILD_BOT",
                    "params": {
                    "d_loc": [(random.choice([-2, 2]),random.choice([-2, 2]))]
                    }
                    })
            elif a.check_balance(game_DB, 600) and sum(agent["warehouse"].values()) < 3:
                return jsonify({
                    "type": "ASSEMBLE_POWER_PLANT",
                    "params": {
                    "power_type": "SOLAR_PANELS"
                    }
                    })
            else:
                return jsonify({'type': 'None'})

    if agent['type'] == "ENGINEER_BOT":
        x, y = agent['location']
        if game_DB['round'] in [1, 10, 20]: 
            return jsonify({
                "type": "EXPLORE",
                "params": {}
                })

        elif game_DB['round'] // 2 == 0:
            return jsonify({
                "type": "MOVE",
                "params": {
                "d_loc": [random.choice([-2, 2]), random.choice([-2, 2])]
                }
                })
        
        elif game_DB['round'] // 2 != 0 and a.check_position(agents, 'WINDMILL'): 
            return jsonify({
                "type": "DEPLOY",
                "params": {
                    "power_type": "WINDMILL",
                    "d_loc": random.choice([[-1, 0], [0, -1], [1, 0], [0, 1]])
                }
                })
        elif game_DB['round'] // 2 != 0 and a.check_position(agents, "SOLAR_PANELS"): 
            if map[x][y] == 'DESERT' or map[x][y] == 'PLAINS':
                return jsonify({
                    "type": "DEPLOY",
                    "params": {
                        "power_type": "SOLAR_PANELS",
                        "d_loc": random.choice([[-1, 0], [0, -1], [1, 0], [0, 1]])
                    }
                    })
            else:
                return jsonify({
                    "type": "MOVE",
                    "params": {
                    "d_loc": [random.choice([-2, 2]), random.choice([-2, 2])]
                    }
                    })
            
        else:        
            return jsonify({'type': 'None'})


@app.route('/agent/<int:id>', methods=['DELETE'])
def toDeleteAgent(id: int):
    del agents[id]
    return Response(status=200)


@app.route('/agent/<int:id>/view', methods=['POST'])
def toExplore(id: int):
    r = request.get_json()
    for i in r['map']:
        for j in i:
            x, y = j['location']
            map[x][y] = j
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
