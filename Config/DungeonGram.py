from dungeongrams.dungeongrams import *
from Game.DungeonGram.IO import get_levels
from Game.DungeonGram.Behavior import *
from Utility import NGram
from Utility.GridTools import columns_into_rows
from Utility.LinkerGeneration import *

from dungeongrams import *

name = 'DungeonGrams'
data_dir = f'DungeonData'

fitness = lambda lvl: get_fitness(lvl, get_percent_playable(lvl))
is_vertical = False
resolution = 40

n = 3
gram = NGram(n)
unigram = NGram(1)
levels = get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

ELITES_PER_BIN = 4

unigram_keys = set(unigram.grammar[()].keys())
pruned = gram.fully_connect() # remove dead ends from grammar
unigram_keys.difference_update(pruned) # remove any n-gram dead ends from unigram

max_path_length = 4

def get_percent_playable(level, thorough=False, agent=None):
    # if agent == None:
    #     agent = FLAW_NO_FLAW

    # return percent_playable(columns_into_rows(level), False, True, thorough, agent)
    return 1.0

def get_fitness(level, percent_playable, agent=None):
    bad_transitions = gram.count_bad_n_grams(level)
    return bad_transitions + 1 - percent_playable

def __check(c_index, c_length, r_index, r_length, lvl, char, seen_indices):
    if r_index < r_length and c_index < c_length:
        seen_indices.add((c_index, r_index))
        return lvl[c_index][r_index] == char

    return False


def level_is_valid(level):
    # Structure we're looking for
    # //\\
    # \\//
    col_length = len(level)
    row_length = len(level[0])

    seen_indices = set()

    for col_index in range(col_length):
        for row_index in range(row_length):
            cor = (col_index, row_index)
            if cor in seen_indices:
                continue
            
            if level[col_index][row_index] != '\\':
                if level[col_index][row_index] == '/':
                    return False

                seen_indices.add((col_index, row_index))
                continue
            
            if not __check(col_index + 1, col_length, row_index, row_length, level, '\\', seen_indices) or \
               not __check(col_index + 2, col_length, row_index, row_length, level, '/', seen_indices) or \
               not __check(col_index + 3, col_length, row_index, row_length, level, '/', seen_indices) or \
               not __check(col_index, col_length, row_index + 1, row_length, level, '/', seen_indices) or \
               not __check(col_index + 1, col_length, row_index + 1, row_length, level, '/', seen_indices) or \
               not __check(col_index + 2, col_length, row_index + 1, row_length, level, '\\', seen_indices) or \
               not __check(col_index + 3, col_length, row_index + 1, row_length, level, '\\', seen_indices):
               return False

    return True


            