from flask import Flask, Response, jsonify, request
import json
import storage as s
import action as a


app = Flask(__name__)


@app.route('/health')
def getHealth():
    return Response(status=200)


@app.route('/init', methods=['POST'])
def toInit():
    if request.is_json:
        r = request.get_json()
        s.game_database['map_size'] = r['map_size']
        s.game_database['balance'] = r['init_balance']
        s.game_database['team'] = r['team']
        s.map = s.get_map(r['map_size'])
        return Response(status=200)
    else:
        return Response(status=404)
        

@app.route('/round', methods=['POST'])
def toRound():
    if request.is_json:
        r = request.get_json()
        s.game_database['balance'] = r['balance']
        s.game_database['round'] = r['round']
        return Response(status=200)
    else:
        return Response(status=404)
   

@app.route('/agent/<int:id>', methods=['POST'])
def toInitAgent(id: int):
    if request.is_json:
        r = request.get_json()
        s.agents[id] = r
        # x, y = r['location']
        # s.map[x][y] = {r['id'], r['type'], r['team']}
        return Response(status=200)
    else:
        return Response(status=404)


@app.route('/agent/<int:id>', methods=['PATCH'])
def toUpdateAgent(id: int):
    if request.is_json:
        r = request.get_json()
        s.agents[id].update(r)
        return Response(status=200)
    else:
        return Response(status=404)


@app.route('/agent/<int:id>/action', methods=['GET'])
def toGetAction(id: int):
    agent = s.agents[id]
    if agent['type'] == "FACTORY":
        if a.check_round(s.game_database) >= 0 and a.check_amount(s.agents) < 2:
            return jsonify({
                "type": "BUILD_BOT",
                "params": {
                "d_loc": [-1, 3]
                }
                })
        elif a.check_round(s.game_database) >= 1 and a.check_balance(s.game_database, 200) and sum(agent["warehouse"].values()) < 3:
            return jsonify({
                "type": "ASSEMBLE_POWER_PLANT",
                "params": {
                "power_type": "WINDMILL"
                }
                })
        elif a.check_round(s.game_database) >= 30 and a.check_balance(s.game_database, 1000) and sum(agent["warehouse"].values()) < 3:
            return jsonify({
                "type": "ASSEMBLE_POWER_PLANT",
                "params": {
                "power_type": "SOLAR_PANELS"
                }
                })
        else:
            return jsonify({'type': 'None'})


    if agent['type'] == "ENGINEER_BOT":
        if a.check_round(s.game_database) >= 3: # and "WINDMILL" in agent["warehouse"].keys(): 
            return jsonify({
                "type": "DEPLOY",
                "params": {
                    "power_type": "WINDMILL",
                    "d_loc": [-1, 0]
                }
                })
        elif a.check_round(s.game_database) >= 31: #and  "SOLAR_PANELS" in agent["warehouse"].keys(): 
            return jsonify({
                "type": "DEPLOY",
                "params": {
                    "power_type": "SOLAR_PANELS",
                    "d_loc": [0, 1]
                }
                })
        elif a.check_round(s.game_database) == 1: 
            return jsonify({
                "type": "EXPLORE",
                "params": {}
                })
            
        else:
            return jsonify({
                "type": "MOVE",
                "params": {
                "d_loc": [1, 1]
                }
                })
        
    return jsonify({'type': 'None'})


@app.route('/agent/<int:id>', methods=['DELETE'])
def toDeleteAgent(id: int):
    del s.agents[id]
    return Response(status=200)


@app.route('/agent/<int:id>/view', methods=['POST'])
def toExplore(id):
    r = request.get_json()
    for i in r['map']:
        for j in i:
            x, y = j['location']
            s.map[x][y] = j
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
