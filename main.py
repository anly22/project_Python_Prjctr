from flask import Flask, Response, jsonify, request
import random
import action as a


app = Flask(__name__)

game_DB = {
    'balance': None,
    'map_size': None,
    'map': None,
    'team': None,
    'round': 0
    }

agents = {}
plants = {}


@app.route('/health')
def getHealth() -> Response:
    return Response(status=200)


@app.route('/init', methods=['POST'])
def toInit() -> Response:
    if request.is_json:
        r = request.get_json()
        game_DB['map_size'] = r['map_size']
        game_DB['balance'] = r['init_balance']
        game_DB['team'] = r['team']
        size = r['map_size']
        game_DB['map'] = [[None] * size for _ in range(size)]
        print(map)

        global agents, plants
        agents = {}
        plants = {}

        return Response(status=200)
    else:
        return Response(status=400)


@app.route('/round', methods=['POST'])
def toRound() -> Response:
    if request.is_json:
        r = request.get_json()
        game_DB['balance'] = r['balance']
        game_DB['round'] = r['round']
        print(game_DB['round'], agents, plants)
        return Response(status=200)
    else:
        return Response(status=400)


@app.route('/agent/<int:id>', methods=['POST'])
def toInitAgent(id: int) -> Response:
    if request.is_json:
        r = request.get_json()
        # TODO save location to map
        # x, y = r['location']
        if r['type'] == 'FACTORY' or r['type'] == 'ENGINEER_BOT':
            agents[id] = r
            # map[x][y] = {'agent': {agents[id]}}
        elif r['type'] == "POWER_PLANT":
            plants[id] = r
            # map[x][y] = {'agent': {plants[id]}}
        return Response(status=200)
    else:
        return Response(status=400)


@app.route('/agent/<int:id>', methods=['PATCH'])
def toUpdateAgent(id: int) -> Response:
    if request.is_json:
        r = request.get_json()
        agents[id].update(r)
        print(r)
        return Response(status=200)
    else:
        return Response(status=400)


@app.route('/agent/<int:id>/action', methods=['GET'])
def toGetAction(id: int):
    agent = agents[id]
    if agent['type'] == "FACTORY":
        if len(agents) < 2:
            return jsonify({
                "type": "BUILD_BOT",
                "params": {
                        "d_loc": (a.get_d_loc('build'))
                        }
                }), 200
        elif len(agents) == 2 and a.check_balance(game_DB, 250):
            return jsonify({
                "type": "BUILD_BOT",
                "params": {
                        "d_loc": (a.get_d_loc('build'))
                        }
                }), 200
        elif len(agents) >= 2:
            if len(plants) < 10 and a.check_balance(game_DB, 100) and a.check_not_full(agents):
                return jsonify({
                    "type": "ASSEMBLE_POWER_PLANT",
                    "params": {
                            "power_type": "WINDMILL"
                            }
                    }), 200
            elif 10 <= len(plants) <= 15 and a.check_balance(game_DB, 1000) and a.check_not_full(agents):
                return jsonify({
                    "type": "ASSEMBLE_POWER_PLANT",
                    "params": {
                            "power_type": "SOLAR_PANELS"
                            }
                    }), 200
            else:
                return jsonify({
                    "type": "NONE",
                    "params": {}
                    }), 200
        else:
            return jsonify({
                "type": "NONE",
                "params": {}
                }), 200

    if agent['type'] == "ENGINEER_BOT":
        if game_DB['round'] == 2:
            return jsonify({
                "type": "EXPLORE",
                "params": {}
                }), 200
        else:
            if game_DB['round'] % 2 == 0:
                if a.check_position(agents, 'WINDMILL'):
                    return jsonify({
                        "type": "DEPLOY",
                        "params": {
                                "power_type": "WINDMILL",
                                "d_loc": (a.get_d_loc('deploy'))
                                }
                        }), 200
                elif a.check_position(agents, 'SOLAR_PANELS'):
                    return jsonify({
                        "type": "DEPLOY",
                        "params": {
                                "power_type": "SOLAR_PANELS",
                                "d_loc": (a.get_d_loc('deploy'))
                                }
                        }), 200
                else:
                    return jsonify({
                        "type": "MOVE",
                        "params": {
                                "d_loc": (a.get_d_loc('move'))
                                }
                        }), 200
            else:
                return jsonify({
                    "type": "MOVE",
                    "params": {
                            "d_loc": (a.get_d_loc('move'))
                            }
                    }), 200


@app.route('/agent/<int:id>', methods=['DELETE'])
def toDeleteAgent(id: int) -> Response:
    del agents[id]
    return Response(status=200)


@app.route('/agent/<int:id>/view', methods=['POST'])
def toExplore(id: int) -> Response:
    if request.is_json:
        r = request.get_json()
        print(r)
        view = r['map']
        for x in range(game_DB['map_size']):
            for y in range(game_DB['map_size']):
                if view[x][y] is not None:
                    game_DB['map'][x][y] = view[x][y]
        print(map)
        return Response(status=200)
    else:
        return Response(status=400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
