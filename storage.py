import numpy as np

game_database = {'balance': None, 'map_size': None, 'team': None, 'round': 0}

agents = []

# CREATE
map_array = []

def get_map(size: int):
    map_array = np.zeros((size, size))
    return map_array
