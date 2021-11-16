from os.path import join, exists, isdir
from random import seed as random_seed
from Utility.GridTools import columns_into_grid_string

from Utility.LinkerGeneration import *
from Utility import rows_into_columns
from json import load as json_load_file
from sys import exit

class TestLinks:
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
                        bins[key][indices[-1]] = rows_into_columns(level_file.readlines())

        #######################################################################
        print('Loading links...')
        with open(join(DATA_DIR, f'links.json')) as f:
            graph = json_load_file(f)

        #######################################################################
        print('Testing links')
        LINKER = 'tree search'

        count = 0
        playable_counts = {
            'tree search': [0, 0],
            'concatenate': [0, 0]
        }

        valid_counts = {
            'tree search': [0, 0],
            'concatenate': [0, 0]
        }

        valid_and_playable_counts = {
            'tree search': [0, 0],
            'concatenate': [0, 0]
        }

        for src_str in graph:
            src, src_index = self.__string_to_key_and_index(src_str)
            for dst_str in graph[src_str]:
                dst, dst_index = self.__string_to_key_and_index(dst_str)

                # check for counts
                for link_name in playable_counts:
                    if graph[src_str][dst_str][link_name]['link'] == None:
                        level = bins[src][src_index] + bins[dst][dst_index]
                    else:
                        level = bins[src][src_index] + \
                                graph[src_str][dst_str][link_name]['link'] + \
                                bins[dst][dst_index]

                    is_valid = self.config.level_is_valid(level)
                    if is_valid:
                        valid_counts[link_name][0] += 1
                    valid_counts[link_name][1] += 1

                    is_playable = graph[src_str][dst_str][link_name]['percent_playable'] == 1.0
                    if is_playable:
                        playable_counts[link_name][0] += 1
                    playable_counts[link_name][1] += 1

                    if is_valid and is_playable:
                        valid_and_playable_counts[link_name][0] += 1
                    valid_and_playable_counts[link_name][1] += 1

                # this second part is extra error checking so it has some extra 
                # work done but speed isn't a concern
                if graph[src_str][dst_str][LINKER]['percent_playable'] != 1.0:
                    continue
                
                if graph[src_str][dst_str][LINKER]['link'] == None:
                    level = bins[src][src_index] + bins[dst][dst_index]
                else:
                    level = bins[src][src_index] + \
                            graph[src_str][dst_str][LINKER]['link'] + \
                            bins[dst][dst_index]

                # if graph[src_str][dst_str][LINKER]['link'] != []:
                #     print()
                #     for r in reversed(level):
                #         print(r)
                #     print(graph[src_str][dst_str][LINKER]['link'])
                #     exit(-1)

                if not self.config.level_is_valid(level):
                    print('Sequence not possible!')
                    print(f'Source: {src_str}')
                    print(f'Destination: {dst_str}')
                    print(columns_into_grid_string(level))

                    exit(-1)

                count += 1


        print(f'\n{count} links tested and no errors found!\n')
        for link_name in playable_counts:
            print(f'{link_name}:')
            print(f'{valid_counts[link_name][0]} out of {valid_counts[link_name][1]} are valid.')
            print(f'{playable_counts[link_name][0]} out of {playable_counts[link_name][1]} are playable.')
            print(f'{valid_and_playable_counts[link_name][0]} out of {valid_and_playable_counts[link_name][1]} are both.\n')