from Utility.GridTools import columns_into_grid_string
from os.path import join
from os import listdir

def get_levels(lines_to_level):
    levels = []
    base_path = join('dungeongrams', 'train')
    for file_name in listdir(base_path):
        f = open(join(base_path, file_name))
        levels.append(lines_to_level(f.readlines()))
        f.close()

    return levels

def level_to_str(columns):
    return columns_into_grid_string(columns)
