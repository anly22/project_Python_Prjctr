from flask import Flask, Response, jsonify, request
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
        map = [[None] * size for _ in range(size)]
        # print(map)

        global agents
        agents = {}

        return Response(status=200)
    else:
        return Response(status=400)


@app.route('/round', methods=['POST'])
def toRound() -> Response:
    if request.is_json:
        r = request.get_json()
        game_DB['balance'] = r['balance']
        game_DB['round'] = r['round']
        return Response(status=200)
    else:
        return Response(status=400)


@app.route('/agent/<int:id>', methods=['POST'])
def toInitAgent(id: int) -> Response:
    if request.is_json:
        r = request.get_json()
        agents[id] = r
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
        if len(agents) < 3:
            return jsonify({
                "type": "BUILD_BOT",
                "params": {
                        "d_loc": (random.choice([-2, 2]), random.choice([-2, 2]))
                        }
                }), 200
        elif len(agents) >= 3 and a.check_balance(game_DB, 100):
            return jsonify({
                "type": "ASSEMBLE_POWER_PLANT",
                "params": {
                        "power_type": "WINDMILL"
                        }
                }), 200
        else:
            return jsonify({
                "type": "NONE",
                "params": {}
                }), 200

    if agent['type'] == "ENGINEER_BOT":
        if game_DB['round'] in [1, 10, 20]:
            return jsonify({
                "type": "EXPLORE",
                "params": {}
                }), 200
        else:
            if a.check_position(agents, 'WINDMILL'):
                return jsonify({
                    "type": "DEPLOY",
                    "params": {
                            "power_type": "WINDMILL",
                            "d_loc": random.choice([[-1, 0], [0, -1], [1, 0], [0, 1]])
                            }
                    }), 200
            else:
                return jsonify({
                    "type": "MOVE",
                    "params": {
                            "d_loc": (random.choice([0, 2]), random.choice([0, 2]))
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
        # for x in range(game_DB['map_size']):
        #     for y in range(game_DB['map_size']):
        #             if view[x][y] is not None:
        #                 map[x][y] = view[x][y] 
        # for i in view:
        #     for j in i:
        #         x, y = j['location']
        #         map[x][y] = j
        return Response(status=200)
    else:
        return Response(status=400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
