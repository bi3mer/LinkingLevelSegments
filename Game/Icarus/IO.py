from os import listdir
from os.path import join

def get_levels():
    levels = []

    for file_name in listdir(join('vglc_levels', 'Icarus')):
        with open(join('vglc_levels', 'Icarus', file_name)) as f:
            levels.append([l.strip() for l in reversed(f.readlines())])

    return levels

def write_level(f, slices):
    f.write('\n'.join(reversed(slices)))
