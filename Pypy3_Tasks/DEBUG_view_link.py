from json import load as json_load_file
from os.path import join

class DEBUG_view_link:
    def __init__(self, config, alg_type):
        self.alg_type = alg_type
        self.config = config

    def run(self, src, tgt):
        DATA_DIR = join('GramElitesData', self.config.data_dir, self.alg_type)
        LEVEL_DIR =  join(DATA_DIR, 'levels')
        with open(join(LEVEL_DIR, f'{src}.txt'), 'r') as level_file:
            SOURCE = self.config.lines_to_level(level_file.readlines())

        with open(join(LEVEL_DIR, f'{tgt}.txt'), 'r') as level_file:
            TARGET = self.config.lines_to_level(level_file.readlines())

        src = ','.join(src.split('_'))
        tgt = ','.join(tgt.split('_'))

        with open(join(DATA_DIR, f'links.json')) as f:
            links = json_load_file(f)

        LINK = links[src][tgt]['tree search']['link']
        LEVEL = SOURCE + [self.config.BETWEN_LINK_TOKEN] + LINK + [self.config.BETWEN_LINK_TOKEN] + TARGET

        print(self.config.level_to_str(LEVEL))
        print(self.config.level_is_valid(LEVEL))


        
