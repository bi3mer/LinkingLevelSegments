from json import load as json_load_file, dump as json_dump_file
from random import seed as random_seed
from os.path import join, exists, isdir

from Utility.ProgressBar import update_progress
from LinkGeneration import Concatenation, TreeSearch

class GenerateLinks:
    def __init__(self, config, alg_type, seed):
        self.alg_type = alg_type
        self.config = config
        random_seed(seed)

    def __in_bounds(self, coordinate):
        return coordinate[0] >= 0 and coordinate[0] <= self.config.resolution and \
               coordinate[1] >= 0 and coordinate[1] <= self.config.resolution

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
        print('Generating links...')
        DIRECTIONS = ((0,0), (0,1), (0,-1), (1, 0), (-1, 0))
        LINKERS = {
            'concatenate': Concatenation.build_link,
            'tree search': TreeSearch.build_link
        }

        dda_graph = {}
        keys = set(bins.keys())

        i = 0
        link_count = 0

        for k in keys: 
            if i >= 1500: break

            for entry_index, entry in enumerate(bins[k]):
                if entry == None:
                    continue

                str_entry_one = f'{k[0]},{k[1]},{entry_index}'
                if str_entry_one not in dda_graph:
                    dda_graph[str_entry_one] = {}

                for dir in DIRECTIONS:
                    neighbor = (k[0] + dir[0], k[1] + dir[1])
                    while neighbor not in bins:
                        neighbor = (neighbor[0] + dir[0], neighbor[1] + dir[1])
                        
                        if not self.__in_bounds(neighbor):
                            break

                    if neighbor not in bins:
                        continue
                    
                    start = entry
                    for n_index, n_entry in enumerate(bins[neighbor]):
                        update_progress(i/(len(keys)*19))
                        i += 1
                        if i >= 1500: break

                        if n_entry == None:
                            continue

                        # we don't want the possibility for something to connect to itself.config.
                        if dir == (0,0) and n_index == entry_index:
                            continue

                        str_entry_two = f'{neighbor[0]},{neighbor[1]},{n_index}'
                        end = n_entry
                        link_count += 1

                        dda_graph[str_entry_one][str_entry_two] = {}

                        for KEY in LINKERS:
                            link = LINKERS[KEY](start, end, self.config)

                            # case for when no link is found
                            if link == None:
                                dda_graph[str_entry_one][str_entry_two][KEY] = {
                                    'percent_playable': -1,
                                    'link': [],
                                }
                                continue

                            level = start + link + end
                            PERCENT_PLAYABLE = self.config.get_percent_playable(level)
                            if link == []:
                                # link found is empty which means the behavioral characteristics
                                # are perfect
                                dda_graph[str_entry_one][str_entry_two][KEY] = {
                                    'percent_playable': PERCENT_PLAYABLE,
                                    'link': link
                                }
                            else:
                                # otherwise, test behavioral characteristics
                                dda_graph[str_entry_one][str_entry_two][KEY] = {
                                    'percent_playable': PERCENT_PLAYABLE,
                                    'link': link
                                }

            i += 1

        with open(join(DATA_DIR, f'links.json'), 'w') as f:
            json_dump_file(dda_graph, f, indent=1)

