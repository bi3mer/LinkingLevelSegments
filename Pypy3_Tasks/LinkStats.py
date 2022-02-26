from os.path import join, exists, isdir
from random import seed as random_seed

from Utility.LinkerGeneration import *
from json import load as json_load_file

class LinkStats:
    def __init__(self, config, alg_type, seed):
        self.config = config
        self.alg_type = alg_type
        random_seed(seed)

    def run(self):
        print('here!')
        DATA_DIR = join('GramElitesData', self.config.data_dir, self.alg_type)
        LEVEL_DIR =  join(DATA_DIR, 'levels')
        if not exists(LEVEL_DIR) or not isdir(LEVEL_DIR):
            print(f'{LEVEL_DIR} does not exist. Please initialize the submodule first..')
            return
      
        with open(join(DATA_DIR, f'links_{self.config.ALLOW_EMPTY_LINK}.json')) as f:
            graph = json_load_file(f)

        links = {}
        for src_str in graph:
            for dst_str in graph[src_str]:
                l = str(graph[src_str][dst_str]['tree search']['link'])
                if l in links:
                    links[l] += 1
                else:
                    links[l] = 1

        for link in links:
            print(f'{link}: {links[link]}')