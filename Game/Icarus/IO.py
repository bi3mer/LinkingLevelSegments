from os import listdir
from os.path import join

def get_levels(lines_to_level):
    levels = []

    for file_name in listdir(join('vglc_levels', 'Icarus')):
        with open(join('vglc_levels', 'Icarus', file_name)) as f:
            levels.append(lines_to_level(f.readlines()))

    return levels

def level_to_str(slices):
    return '\n'.join(reversed(slices))
