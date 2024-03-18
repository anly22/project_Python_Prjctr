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
    r = request.get_json()
    s.game_database['map_size'] = r.get('map_size', None)
    s.game_database['balance'] = r.get('init_balance', None)
    s.game_database['team'] = r.get('team', None)
    a = r.get('map_size', None)
    s.map_array = s.get_map(a)
    return Response(status=200)
    # return jsonify(s.game_database), 200


@app.route('/round', methods=['POST'])
def toRound():
    r = request.get_json()
    s.game_database['balance'] = r.get('balance', None)
    s.game_database['round'] = r.get('round', None)
    # return Response(status=200)
    return jsonify(s.game_database), 200


@app.route('/agent/<int:id>', methods=['POST'])
def toInitAgent(id):
    agent_info = request.get_json()
    s.agents.append(agent_info)
    # return  jsonify(s.agents), 200
    return Response(status=200)


@app.route('/agent/<int:id>/action', methods=['GET'])
def toCallAgent_Act(id):
    res = jsonify(a.define_action(id))
    res.headers['Content-Type'] = 'application/json'
    return res, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
