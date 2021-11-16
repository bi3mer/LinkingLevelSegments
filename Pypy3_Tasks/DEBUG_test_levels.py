from os.path import join
from os import listdir

from Utility.GridTools import rows_into_columns

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
                level = rows_into_columns(level_file.readlines())

                if self.config.level_is_valid(level) == should_be_invalid:
                    print(f'{join(DATA_DIR, file_name)} does not have the expected result!')
                    test_failed = True
                    import sys
                    sys.exit(-1)

        if not test_failed:
            print('All tests pass!')