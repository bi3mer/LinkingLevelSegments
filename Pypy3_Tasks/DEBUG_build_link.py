from random import seed as random_seed
from os.path import join

from LinkGeneration import TreeSearch

class DEBUG_build_link:
    def __init__(self, config, alg_type, seed):
        self.alg_type = alg_type
        self.config = config
        random_seed(seed)

    def run(self, path):
        # sample_path: 3,10,1|2,10,1|2,11,2
        DATA_DIR = join('GramElitesData', self.config.data_dir, self.alg_type)
        LEVEL_DIR =  join(DATA_DIR, 'levels')

        nodes = path.split('|')
        segments = []

        for link_name in nodes:
            fname = '_'.join(link_name.split(','))
            with open(join(LEVEL_DIR, f'{fname}.txt'), 'r') as level_file:
                segments.append(self.config.lines_to_level(level_file.readlines()))
        
        print_lvl = segments[0].copy()
        play_lvl = segments[0].copy()

        for i in range(1, len(segments)):
            LINKER = TreeSearch.build_link(segments[i-1], segments[i], self.config)
            print_lvl += [self.config.BETWEEN_LINK_TOKEN]
            print_lvl += LINKER
            print_lvl += [self.config.BETWEEN_LINK_TOKEN]            
            print_lvl += segments[i].copy()

            play_lvl += LINKER
            play_lvl += segments[i].copy()

        print(self.config.level_to_str(print_lvl))
        print()
        print(f'is valid: {self.config.level_is_valid(play_lvl)}')
        print(f'playable: {self.config.get_percent_playable(play_lvl)}')
        print()
