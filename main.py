from flask import Flask, Response, jsonify, request
import utils as u


app = Flask(__name__)

game_DB = {
    'balance': None,
    'map_size': None,
    'map': None,
    'team': None,
    'round': 0
    }

agents: dict = {}
plants: dict = {}


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
        game_DB['map'] = [[None] * size for _ in range(size)]  # type: ignore

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
        x, y = r['location']
        if r['type'] == 'FACTORY':
            agents[id] = r
            game_DB['map'][x][y] = {'type': None,  # type: ignore
                                    'agent': agents[id]}
        elif r['type'] == 'ENGINEER_BOT':
            agents[id] = r
        elif r['type'] == "POWER_PLANT":
            plants[id] = r
            game_DB['map'][x][y] = {'type': None,  # type: ignore
                                    'agent': plants[id]}
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


def toGetActionFactory() -> tuple[Response, int]:
    if len(agents) < 2:
        return jsonify({
            "type": "BUILD_BOT",
            "params": {
                    "d_loc": (u.get_d_loc('build'))
                    }
            }), 200
    elif 2 <= len(agents) < 3 and u.get_balance(game_DB, 400):
        return jsonify({
            "type": "BUILD_BOT",
            "params": {
                    "d_loc": (u.get_d_loc('build'))
                    }
            }), 200
    else:
        if u.get_warehouse_not_full(agents):
            if u.get_near(game_DB['map'],  # type: ignore
                          u.get_loc(agents, 'ENGINEER_BOT'),
                          'DESERT') and u.get_balance(game_DB, 800):
                return jsonify({
                    "type": "ASSEMBLE_POWER_PLANT",
                    "params": {
                            "power_type": "SOLAR_PANELS"
                            }
                    }), 200
            elif u.get_near(game_DB['map'],  # type: ignore
                            u.get_loc(agents, 'ENGINEER_BOT'),
                            'MOUNTAIN') and u.get_balance(game_DB, 800):
                return jsonify({
                    "type": "ASSEMBLE_POWER_PLANT",
                    "params": {
                            "power_type": "GEOTHERMAL"
                            }
                    }), 200
            elif u.get_near(game_DB['map'],  # type: ignore
                            u.get_loc(agents, 'ENGINEER_BOT'),
                            'RIVER'):
                if u.get_balance(game_DB, 1200) and \
                        u.get_power_type(plants, 'DAM') < 1:
                    return jsonify({
                        "type": "ASSEMBLE_POWER_PLANT",
                        "params": {
                                "power_type": "DAM"
                                }
                        }), 200
                else:
                    return jsonify({
                        "type": "NONE",
                        "params": {}
                        }), 200
            elif u.get_balance(game_DB, 120):
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
        else:
            return jsonify({
                        "type": "NONE",
                        "params": {}
                        }), 200


def toGetActionEngineer() -> tuple[Response, int]:
    if game_DB['round'] in [3, 19, 49, 89, 119, 149, 179, 299, 399]:
        return jsonify({
            "type": "EXPLORE",
            "params": {}
            }), 200
    elif game_DB['round'] % 2 != 0:  # type: ignore
        return jsonify({
                        "type": "MOVE",
                        "params": {
                                "d_loc": (u.get_d_loc('move'))
                                }
                        }), 200
    else:
        if u.get_plant_in_warehouse(agents, 'WINDMILL') and \
            u.get_near(game_DB['map'],  # type: ignore
                       u.get_loc(agents, 'ENGINEER_BOT'),
                       'OCEAN'):
            return jsonify({
                    "type": "DEPLOY",
                    "params": {
                            "power_type": "WINDMILL",
                            "d_loc": (u.get_near_loc(game_DB['map'],  # type: ignore
                                                     u.get_loc(agents, 'ENGINEER_BOT'),
                                                     'OCEAN'))
                            }
                    }), 200
        elif u.get_plant_in_warehouse(agents, 'SOLAR_PANELS') and \
            u.get_near(game_DB['map'],  # type: ignore
                       u.get_loc(agents, 'ENGINEER_BOT'),
                       'DESERT'):
            return jsonify({
                    "type": "DEPLOY",
                    "params": {
                            "power_type": "SOLAR_PANELS",
                            "d_loc": (u.get_near_loc(game_DB['map'],  # type: ignore
                                                     u.get_loc(agents, 'ENGINEER_BOT'),
                                                     'DESERT'))
                            }
                    }), 200
        elif u.get_plant_in_warehouse(agents, 'GEOTHERMAL') and \
            u.get_near(game_DB['map'],  # type: ignore
                       u.get_loc(agents, 'ENGINEER_BOT'),
                       'MOUNTAIN'):
            return jsonify({
                    "type": "DEPLOY",
                    "params": {
                            "power_type": "GEOTHERMAL",
                            "d_loc": (u.get_near_loc(game_DB['map'],  # type: ignore
                                                     u.get_loc(agents, 'ENGINEER_BOT'),
                                                     'MOUNTAIN'))
                            }
                    }), 200
        elif u.get_plant_in_warehouse(agents, 'DAM') and \
            u.get_near(game_DB['map'],  # type: ignore
                       u.get_loc(agents, 'ENGINEER_BOT'),
                       'RIVER'):
            return jsonify({
                    "type": "DEPLOY",
                    "params": {
                            "power_type": "DAM",
                            "d_loc": (u.get_near_loc(game_DB['map'],  # type: ignore
                                                     u.get_loc(agents, 'ENGINEER_BOT'),
                                                     'RIVER'))
                            }
                    }), 200
        else:
            if u.get_plant_in_warehouse(agents, 'WINDMILL'):  # type: ignore
                return jsonify({
                        "type": "DEPLOY",
                        "params": {
                                "power_type": "WINDMILL",
                                "d_loc": (u.get_d_loc('deploy'))
                                }
                        }), 200
            else:
                return jsonify({
                        "type": "MOVE",
                        "params": {
                                "d_loc": (u.get_d_loc('move'))
                                }
                        }), 200


@app.route('/agent/<int:id>/action', methods=['GET'])
def toGetAction(id: int) -> tuple[Response, int] | Response:
    agent = agents[id]
    if agent['type'] == "FACTORY":
        return toGetActionFactory()
    elif agent['type'] == "ENGINEER_BOT":
        return toGetActionEngineer()
    else:
        return Response(status=400)


@app.route('/agent/<int:id>', methods=['DELETE'])
def toDeleteAgent(id: int) -> Response:
    del agents[id]
    return Response(status=200)


@app.route('/agent/<int:id>/view', methods=['POST'])
def toExplore(id: int) -> Response:
    if request.is_json:
        r = request.get_json()
        view = r['map']
        for x in range(game_DB['map_size']):  # type: ignore
            for y in range(game_DB['map_size']):  # type: ignore
                if view[x][y] is not None:
                    game_DB['map'][x][y] = view[x][y]  # type: ignore
        print(game_DB['map'])
        return Response(status=200)
    else:
        return Response(status=400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
