from flask import Flask, Response, jsonify, request
import json
# import numpy as np
import storage as s
import actions as a

app = Flask(__name__)


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
        a = r['map_size']
        s.map_array = s.get_map(a)
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
        print(s.agents)
        # return  jsonify(s.agents), 200
        return Response(status=200)
    else:
        return Response(status=404)


@app.route('/agent/<int:id>/action', methods=['GET'])
def toCallAgent_Act(id):
    res = jsonify(a.define_action(id))
    res.headers['Content-Type'] = 'application/json'

    for a in s.agents: 
        print(a, 'AGENTS')
        
    return res, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
