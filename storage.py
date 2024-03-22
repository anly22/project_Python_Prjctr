# import numpy as np


game_database = {
    'balance': None,
    'map_size': None,
    'team': None,
    'round': 0
    }


agents = {}
# agents = []


map = []


def get_map(size: int):
    map = [[None] * size for _ in range(size)]
    return map
