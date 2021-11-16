from random import seed as random_seed
from LinkGeneration import TreeSearch

class DEBUG_build_link:
    def __init__(self, config, alg_type, seed):
        self.alg_type = alg_type
        self.config = config
        random_seed(seed)

    def run(self):
        f = open('temp.txt')
        lvl = self.config.lines_to_level(f.readlines())
        f.close()

        link = TreeSearch.build_link(lvl, lvl, self.config)
        
        print(self.config.level_to_str(lvl + link + lvl))
        
