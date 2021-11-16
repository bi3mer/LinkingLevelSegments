from dungeongrams.dungeongrams import *
from Game.Icarus.IO import get_levels
from Game.Icarus.Behavior import *
from Game.Icarus.Fitness import *
from Utility import NGram
from Utility.LinkerGeneration import *
from dungeongrams import *

name = 'Icarus'
data_dir = 'IcarusData'

resolution = 40

def lines_to_level(lines):
    return[l.strip() for l in reversed(lines)]

n = 2
gram = NGram(n)
unigram = NGram(1)
levels = get_levels(lines_to_level)
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

ELITES_PER_BIN = 4

unigram_keys = set(unigram.grammar[()].keys())
pruned = gram.fully_connect() # remove dead ends from grammar
unigram_keys.difference_update(pruned) # remove any n-gram dead ends from unigram

link_keys = unigram_keys
link_keys = [
    '----------------',
    '---TTTT--TTTT---',
    'TTT----TT----TTT'
]
for row in unigram_keys:
    if 'd' in row or 'D' in row:
        link_keys.append(row)

fitness = lambda level: get_fitness(level, get_percent_playable(level))
is_vertical = True

max_path_length = 4

__percent_completable = build_slow_fitness_function(gram)
def get_percent_playable(level, agent=None):
    return __percent_completable(level)

def get_fitness(level, percent_playable, agent=None):
    bad_n_grams = gram.count_bad_n_grams(level)
    return bad_n_grams + 1 - percent_playable

def level_is_valid(level):
    num_columns = len(level[0])
    seen = set()
    for row_index in range(len(level)):
        for col_index in range(num_columns):
            current_char = level[row_index][col_index]
            if current_char != 'D' and current_char != 'd':
                continue

            if (row_index, col_index) in seen:
                continue

            # Case 1: Door is incomplete at the start D|d---
            if col_index == 0 and current_char == 'd':
                seen.add((row_index, col_index))
            
            # case 2: door is incomplete at end ------D|d
            elif col_index == len(level[0]) - 1: 
                if current_char == 'D':
                    seen.add((row_index, col_index)) # technically not necessary
            
            # Case 3: door is full, Dd
            elif current_char == 'D' and level[row_index][col_index + 1] == 'd':
                seen.add((row_index, col_index))
                seen.add((row_index, col_index + 1))
            else:
                return False

    return True

