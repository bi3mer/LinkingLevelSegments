from random import seed as random_seed
from os.path import join

from LinkGeneration import TreeSearch

class DEBUG_build_link:
    def __init__(self, config, alg_type, seed):
        self.alg_type = alg_type
        self.config = config
        random_seed(seed)

    def run(self, src, tgt):
        DATA_DIR = join('GramElitesData', self.config.data_dir, self.alg_type)
        LEVEL_DIR =  join(DATA_DIR, 'levels')
        with open(join(LEVEL_DIR, f'{src}.txt'), 'r') as level_file:
            SOURCE = self.config.lines_to_level(level_file.readlines())

        with open(join(LEVEL_DIR, f'{tgt}.txt'), 'r') as level_file:
            TARGET = self.config.lines_to_level(level_file.readlines())

        src = ','.join(src.split('_'))
        tgt = ','.join(tgt.split('_'))


        LINK = TreeSearch.build_link(SOURCE, TARGET, self.config)


        LEVEL = SOURCE + [self.config.BETWEN_LINK_TOKEN] + LINK + [self.config.BETWEN_LINK_TOKEN] + TARGET

        print(self.config.level_to_str(LEVEL))
        print(self.config.level_is_valid(LEVEL))

        # f = open('temp.txt')
        # lvl = self.config.lines_to_level(f.readlines())
        # f.close()

        # print(self.config.level_to_str(lvl))

        
        # print(self.config.level_to_str(lvl + link + lvl))
        
