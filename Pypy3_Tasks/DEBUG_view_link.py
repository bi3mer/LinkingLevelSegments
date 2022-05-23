from json import load as json_load_file
from os.path import join

class DEBUG_view_link:
    def __init__(self, config, alg_type):
        self.alg_type = alg_type
        self.config = config

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
        
        link_file = join(DATA_DIR, f'links_{self.config.ALLOW_EMPTY_LINK}.json')
        print(f'Reading links: {link_file}')
        with open(link_file) as f:
            links = json_load_file(f)

        level = segments[0]
        for i in range(1, len(nodes)):
            print(nodes[i-1], nodes[i])
            level += [self.config.BETWEEN_LINK_TOKEN]
            level += links[nodes[i-1]][nodes[i]]['tree search']['link'] 
            level += [self.config.BETWEEN_LINK_TOKEN]            
            level += segments[i]

        # LEVEL = SOURCE + [self.config.BETWEEN_LINK_TOKEN] + LINK + [self.config.BETWEEN_LINK_TOKEN] + TARGET

        print(self.config.level_to_str(level))
        print(self.config.level_is_valid(level))


        
