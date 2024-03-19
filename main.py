from flask import Flask, Response, jsonify, request
import json
import numpy as np
import storage as s


app = Flask(__name__)

# game_database = {
#     'balance': None,
#     'map_size': None,
#     'team': None,
#     'round': 0
#     }

# agents = []

# map_array = []


def get_map(size: int):
    map_array = np.zeros((size, size))
    return map_array
@app.route('/health')
def gethealth():
    return Response(status=200)


@app.route('/init', methods=['POST'])
def toInit():
    if request.is_json:
        r = request.get_json()
        s.game_database['map_size'] = r['map_size']
        s.game_database['balance'] = r['init_balance']
        s.game_database['team'] = r['team']
        s.map_array = get_map(r['map_size'])
        print("INIT", s.game_database)
        return Response(status=200)
    else:
        return Response(status=404)
        # return jsonify(s.game_database), 200


@app.route('/round', methods=['POST'])
def toRound():
    if request.is_json:
        r = request.get_json()
        s.game_database['balance'] = r['balance']
        s.game_database['round'] = r['round']
        print('ROUND', s.game_database)
        return Response(status=200)
    else:
        return Response(status=404)
    # return jsonify(s.game_database), 200


@app.route('/agent/<int:id>', methods=['POST'])
def toInitAgent(id):
    if request.is_json:
        agent_info = request.get_json()
        s.agents.append(agent_info)
        for a in s.agents: 
            print('AGENT', a)
        # return  jsonify(s.agents), 200
        return Response(status=200)
    else:
        return Response(status=404)


@app.route('/agent/<int:id>/action', methods=['GET'])
def toCallAct(id):
    print(id, 'BUILD BOT AGENT')
    build = jsonify({"type": "BUILD_BOT", "params": {"d_loc": [-1, 1]}})

    return build, 200
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
