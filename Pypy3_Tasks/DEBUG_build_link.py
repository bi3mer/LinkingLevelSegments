from random import seed as random_seed
from LinkGeneration import TreeSearch

class DEBUG_build_link:
    def __init__(self, config, alg_type, seed):
        self.alg_type = alg_type
        self.config = config
        random_seed(seed)

    def run(self):
        start = self.config.levels[0][5:20]
        end = self.config.levels[1][5:25]

        for a in end:
            print(a)

        print('|||||||||||||||||||')
        link = TreeSearch.build_link(start, end, self.config)
        print(link)
        print('|||||||||||||||||||')

        for a in start:
            print(a)
        
