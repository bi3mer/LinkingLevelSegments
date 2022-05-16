from os.path import join, exists, isdir
from random import seed as random_seed

from Utility.LinkerGeneration import *
from json import load as json_load_file

class LinkStats:
    def __init__(self, config, alg_type, seed):
        self.config = config
        self.alg_type = alg_type
        random_seed(seed)

    def __string_to_key_and_index(self, string):
        split = string.split(',')
        return tuple([int(val) for val in split[:-1]]), int(split[-1])

    def run(self):
        #######################################################################
        DATA_DIR = join('GramElitesData', self.config.data_dir, self.alg_type)
        LEVEL_DIR =  join(DATA_DIR, 'levels')
        if not exists(LEVEL_DIR) or not isdir(LEVEL_DIR):
            print(f'{LEVEL_DIR} does not exist. Please initialize the submodule first..')
            return

        #######################################################################
        bins = {}
        with open(join(DATA_DIR, 'generate_corpus_info.json')) as f:
            data = json_load_file(f)
            for file_name in data['fitness']:
                if data['fitness'][file_name] == 0.0:
                    # remove the .txt extension and take all indices except the last one
                    indices = [int(num) for num in file_name[:-4].split('_')]
                    key = tuple(indices[:-1])

                    if key not in bins:
                        bins[key] = [None for _ in range(self.config.ELITES_PER_BIN)]
                    
                    with open(join(LEVEL_DIR, file_name), 'r') as level_file:
                        bins[key][indices[-1]] = self.config.lines_to_level(level_file.readlines())
      
        #######################################################################
        with open(join(DATA_DIR, f'links_{self.config.ALLOW_EMPTY_LINK}.json')) as f:
            graph = json_load_file(f)

        #######################################################################
        print(f'Average link length')
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

        #######################################################################
        print('\nAverage Length')
        length = 0
        total = 0
        max_length = 0

        for src_str in graph:
            for dst_str in graph[src_str]:
                l = graph[src_str][dst_str]['tree search']['link']
                
                max_length = max(max_length, len(l))
                length += len(l)
                total +=1

        print(f'Average Link Length: {length / total}')
        print(f'Max Length: {max_length}')

        #######################################################################
        print('\nBehavioral Charecteristics')
        res = {}
        for name in self.config.FEATURE_NAMES:
            res[name] = 0

        total = 0

        for src_str in graph:
            src, src_index = self.__string_to_key_and_index(src_str)
            src_lvl = bins[src][src_index]

            for dst_str in graph[src_str]:
                dst, dst_index = self.__string_to_key_and_index(src_str)
                dst_lvl = bins[dst][dst_index]
                l = graph[src_str][dst_str]['tree search']['link']
                
                concatenated_lvl = src_lvl + dst_lvl
                linked_lvl = src_lvl + l + dst_lvl

                for name, f in zip(self.config.FEATURE_NAMES, self.config.FEATURE_DESCRIPTORS):
                     res[name] += abs(f(linked_lvl) - f(concatenated_lvl))

                total += 1

        for name in self.config.FEATURE_NAMES:
            print(f'{name}: {res[name] / total}')


