from os.path import join, exists, isdir

from Utility.LinkerGeneration import *
from json import load as json_load_file


class DEBUG_largest_link:
    def __init__(self, config, alg_type):
        self.alg_type = alg_type
        self.config = config

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
        src = None
        src_info = None
        dst = None
        dst_info = None
        link = []
        for src_str in graph:
            for dst_str in graph[src_str]:
                l = graph[src_str][dst_str]['tree search']['link']
                if len(l) > len(link):
                    src_info = src_str
                    dst_info = dst_str 

                    src_key, src_index = self.__string_to_key_and_index(src_str)
                    dst_key, dst_index = self.__string_to_key_and_index(dst_str)

                    src = bins[src_key][src_index]
                    dst = bins[dst_key][dst_index]
                    link = l

        concatenated_lvl = src + dst
        linked_lvl = src + [self.config.BETWEEN_LINK_TOKEN] + link + [self.config.BETWEEN_LINK_TOKEN] + dst

        print(src_info)
        print(dst_info)
        print('Concatenated')
        print(self.config.level_to_str(concatenated_lvl))
        print('\n\n\nLinked')
        print(self.config.level_to_str(linked_lvl))


