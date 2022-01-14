from os.path import join, exists, isdir
from random import seed as random_seed
from json import load as json_load_file

from Utility.Math import *

class WalkthroughStats:
    def __init__(self, config, alg_type, seed):
        self.config = config
        self.alg_type = alg_type
        random_seed(seed)

    def run(self):
        DATA_DIR = join('GramElitesData', self.config.data_dir, self.alg_type)
        LEVEL_DIR =  join(DATA_DIR, 'levels')
        if not exists(LEVEL_DIR) or not isdir(LEVEL_DIR):
            print(f'{LEVEL_DIR} does not exist. Please initialize the submodule first..')
            return
      
        with open(join(DATA_DIR, f'walkthrough.json')) as f:
            graph = json_load_file(f)

        for k in sorted(list(graph.keys())):
            scores = [1 if graph[k][sequence] == 1.0 else 0 for sequence in graph[k]]

            print(f'K={k}')
            print(f'min: {min(scores)}')
            print(f'max: {max(scores)}')
            print(f'mean: {mean(scores)}')
            print(f'median: {median(scores)}')
            print()
            print()
