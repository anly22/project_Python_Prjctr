from flask import Flask, Response, jsonify, request
import json
import random
# import storage as s
import action as a


app = Flask(__name__)

game_database = {
    'balance': None,
    'map_size': None,
    'team': None,
    'round': 0
    }

agents = {}

map = []

def get_map(size: int):
    map = [[None] * size for _ in range(size)]
    return map


@app.route('/health')
def getHealth():
    return Response(status=200)


@app.route('/init', methods=['POST'])
def toInit():
    if request.is_json:
        r = request.get_json()
        game_database['map_size'] = r['map_size']
        game_database['balance'] = r['init_balance']
        game_database['team'] = r['team']
        map = get_map(r['map_size'])

        global agents
        agents = {}

        return Response(status=200)
    else:
        return Response(status=404)
        

@app.route('/round', methods=['POST'])
def toRound():
    if request.is_json:
        r = request.get_json()
        game_database['balance'] = r['balance']
        game_database['round'] = r['round']
        return Response(status=200)
    else:
        return Response(status=404)
   

@app.route('/agent/<int:id>', methods=['POST'])
def toInitAgent(id: int):
    if request.is_json:
        r = request.get_json()
        agents[id] = r
        # x, y = r['location']
        # s.map[x][y] = {r['id'], r['type'], r['team']}
        return Response(status=200)
    else:
        return Response(status=404)


@app.route('/agent/<int:id>', methods=['PATCH'])
def toUpdateAgent(id: int):
    if request.is_json:
        r = request.get_json()
        agents[id].update(r)
        return Response(status=200)
    else:
        return Response(status=404)


@app.route('/agent/<int:id>/action', methods=['GET'])
def toGetAction(id: int):
    agent = agents[id]
    if agent['type'] == "FACTORY":
        if a.check_round(game_database) >= 0 and a.check_amount(agents) < 2:
            return jsonify({
                "type": "BUILD_BOT",
                "params": {
                "d_loc": (random.choice([-1, 3]),random.choice([-1, 3]))
                }
                })
        elif a.check_round(game_database) >= 1 and a.check_balance(game_database, 200) and sum(agent["warehouse"].values()) < 3:
            return jsonify({
                "type": "ASSEMBLE_POWER_PLANT",
                "params": {
                "power_type": "WINDMILL"
                }
                })
        elif a.check_round(game_database) >= 30 and a.check_balance(game_database, 1000) and sum(agent["warehouse"].values()) < 3:
            return jsonify({
                "type": "ASSEMBLE_POWER_PLANT",
                "params": {
                "power_type": "SOLAR_PANELS"
                }
                })
        else:
            return jsonify({'type': 'None'})


    if agent['type'] == "ENGINEER_BOT":
        if a.check_round(game_database) >= 3: # and "WINDMILL" in agent["warehouse"].keys(): 
            return jsonify({
                "type": "DEPLOY",
                "params": {
                    "power_type": "WINDMILL",
                    "d_loc": random.choice([-1, 0],[0, -1], [1, 0], [0, 1])
                }
                })
        elif a.check_round(game_database) >= 31: #and  "SOLAR_PANELS" in agent["warehouse"].keys(): 
            return jsonify({
                "type": "DEPLOY",
                "params": {
                    "power_type": "SOLAR_PANELS",
                    "d_loc": random.choice([-1, 0],[0, -1], [1, 0], [0, 1])
                }
                })
        elif a.check_round(game_database) == 1: 
            return jsonify({
                "type": "EXPLORE",
                "params": {}
                })
            
        else:
            return jsonify({
                "type": "MOVE",
                "params": {
                "d_loc": random.choice([-1, 0],[0, -1], [1, 0], [0, 1])
                }
                })
        
    return jsonify({'type': 'None'})


@app.route('/agent/<int:id>', methods=['DELETE'])
def toDeleteAgent(id: int):
    del agents[id]
    return Response(status=200)


@app.route('/agent/<int:id>/view', methods=['POST'])
def toExplore(id):
    r = request.get_json()
    for i in r['map']:
        for j in i:
            x, y = j['location']
            map[x][y] = j
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
