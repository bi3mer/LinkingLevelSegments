from Utility.GridTools import columns_into_grid_string
import os

def get_levels(lines_to_level):
    levels = []
    skip_levels = [
        'mario-1-2.txt', 'mario-1-3.txt', 'mario-2-1.txt', 'mario-3-3.txt', 
        'mario-4-2.txt', 'mario-4-3.txt', 'mario-5-3.txt', 'mario-6-3.txt',
        'mario-8-2.txt'
    ]

    for file_name in os.listdir(os.path.join('vglc_levels', 'Mario')):
        if file_name in skip_levels:
            continue
            
        f = open(os.path.join('vglc_levels', 'Mario', file_name))
        levels.append(lines_to_level(f.readlines()))
        f.close()

    return levels

def level_to_str(columns):
    return columns_into_grid_string(columns)
