from os.path import join, exists, isdir
from random import seed as random_seed, shuffle
from json import load as json_load_file, dump as json_dump_file
from random import choice
from os.path import join
from sys import exit

from Utility.LinkerGeneration import *
from Utility.Math import *
from Utility.ProgressBar import update_progress
from dungeongrams.dungeongrams import play

class Walkthrough:
    def __init__(self, config, alg_type, seed):
        self.config = config
        self.alg_type = alg_type
        random_seed(seed)

    def __string_to_key_and_index(self, string):
        split = string.split(',')
        return tuple([int(val) for val in split[:-1]]), int(split[-1])

    def run(self):
        #######################################################################
        print('Checking directory structure...')
        DATA_DIR = join('GramElitesData', self.config.data_dir, self.alg_type)
        LEVEL_DIR =  join(DATA_DIR, 'levels')
        if not exists(LEVEL_DIR) or not isdir(LEVEL_DIR):
            print(f'{LEVEL_DIR} does not exist. Please initialize the submodule first..')
            return

        #######################################################################
        print('Loading bins...')
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
        print('Loading links...')
        with open(join(DATA_DIR, f'links.json')) as f:
            graph = json_load_file(f)

        #######################################################################
        print('Running Walkthrough')
        TOTAL = 1000
        playability_scores = {}
        src_keys = list(graph.keys())

        for k in range(2,6): 
            print(f'K={k}')
        
            levels_found = 0
            playability_scores[k] = {}
        
            while levels_found < TOTAL:
                src_str = choice(src_keys)
                sequence_keys = [src_str]
                src, src_index = self.__string_to_key_and_index(src_str)
                level = bins[src][src_index].copy()
                full_level = True

                for __ in range(1, k):
                    if src_str not in graph:
                        full_level = False
                        break
                    
                    found = False
                    keys = list(graph[src_str].keys())
                    shuffle(keys)

                    for dst_str in keys:
                        if graph[src_str][dst_str]['tree search']['percent_playable'] == 1.0:
                            found = True
                            dst, dst_index = self.__string_to_key_and_index(dst_str)
                            
                            __test_level = bins[src][src_index].copy()
                            if graph[src_str][dst_str]['tree search']['link'] == None:
                                level += bins[dst][dst_index]
                                __test_level += bins[dst][dst_index]
                            else:
                                level += graph[src_str][dst_str]['tree search']['link'] + bins[dst][dst_index]
                                __test_level += graph[src_str][dst_str]['tree search']['link'] + bins[dst][dst_index]

                            # error checking
                            __playability = self.config.get_percent_playable(__test_level)
                            if __playability != 1.0:
                                print(self.config.level_to_str(__test_level))
                                print(f'{src_str} -> {dst_str} has playability of {__playability} but should have 1.')
                                exit(-1)

                            sequence_keys.append(dst_str)
                            src_str = dst_str
                            src, src_index = self.__string_to_key_and_index(src_str)
                            break

                    if not found:
                        full_level = False
                        break
                    
                if full_level:
                    assert self.config.level_is_valid(level)
                    sequence_key = '|'.join(sequence_keys)
                    if sequence_key not in playability_scores:
                        levels_found += 1
                        playability_scores[k][sequence_key] = self.config.get_percent_playable(level)
                        update_progress(levels_found/TOTAL)


        with open(join(DATA_DIR, 'walkthrough.json'), 'w') as f:
            json_dump_file(playability_scores, f, indent=2)

        print()

        for k in range(2, 6):
            scores = [s for s in playability_scores[k].values()]
            print(f'K={k}')
            print(f'min: {min(scores)}')
            print(f'max: {max(scores)}')
            print(f'mean: {mean(scores)}')
            print(f'median: {median(scores)}')
            print()
            print()
