from distutils.command.config import config
from os.path import join
from os import listdir

class DEBUG_test_levels:
    def __init__(self, config, alg_type):
        self.alg_type = alg_type
        self.config = config

    def run(self):
        DATA_DIR = join('test_levels', self.config.data_dir)
        test_failed = False

        for file_name in listdir(DATA_DIR):
            if not file_name.endswith('.txt'):
                continue
            
            should_be_invalid = 'invalid' in file_name
            with open(join(DATA_DIR, file_name), 'r') as level_file:
                level = self.config.lines_to_level(level_file.readlines())

                if self.config.level_is_valid(level) == should_be_invalid:
                    temp = self.config.get_percent_playable(level)
                    print(f'{join(DATA_DIR, file_name)} was not generable by an n-gram and was {temp:0.03f}% completable')
                    test_failed = True


        if not test_failed:
            print('All tests pass!')