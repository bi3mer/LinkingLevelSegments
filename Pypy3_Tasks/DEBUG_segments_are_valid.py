from json import load as json_load_file
from random import seed as random_seed
from os.path import join
from sys import exit

class DEBUG_segments_are_valid:
    def __init__(self, config, alg_type, seed):
        self.alg_type = alg_type
        self.config = config
        random_seed(seed)

    def run(self):
        DATA_DIR = join('GramElitesData', self.config.data_dir, self.alg_type)
        LEVEL_DIR =  join(DATA_DIR, 'levels')

        with open(join(DATA_DIR, 'generate_corpus_info.json')) as f:
            data = json_load_file(f)
            for file_name in data['fitness']:
                with open(join(LEVEL_DIR, file_name), 'r') as level_file:
                    level = self.config.lines_to_level(level_file.readlines())

                    if not self.config.level_is_valid(level):
                        print(self.config.level_to_str(level))
                        print(f'{join(LEVEL_DIR, file_name)} is not valid!')
                        exit(-1)
