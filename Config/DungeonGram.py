from dungeongrams.dungeongrams import *
from Game.DungeonGram.IO import get_levels
from Game.DungeonGram.Behavior import *
from Utility import NGram
from Utility.LinkerGeneration import *
from Utility.GridTools import columns_into_rows, rows_into_columns

from dungeongrams import *

name = 'DungeonGrams'
data_dir = f'DungeonData'

fitness = lambda lvl: get_fitness(lvl, get_percent_playable(lvl))
is_vertical = False
resolution = 40

lines_to_level = rows_into_columns

n = 3
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

max_path_length = 4

def get_percent_playable(level, thorough=False, agent=None):
    if agent == None:
        agent = FLAW_NO_FLAW

    return percent_playable(columns_into_rows(level), False, True, thorough, agent)

def get_fitness(level, percent_playable, agent=None):
    bad_transitions = gram.count_bad_n_grams(level)
    return bad_transitions + 1 - percent_playable

def __check(c_index, r_index, lvl, char, seen_indices):
    seen_indices.add((c_index, r_index))
    return lvl[c_index][r_index] == char

def level_is_valid(level):
    # Structure we're looking for
    # //\\
    # \\//
    #
    # I'm not going to claim that this will be the an efficient or 
    # beautiful implementation. I'm looking for something that works.
    col_length = len(level)
    row_length = len(level[0])

    seen_indices = set()

    for col_index in range(col_length):
        for row_index in range(row_length):
            cor = (col_index, row_index)
            if cor in seen_indices:
                continue
            
            char = level[col_index][row_index]
            if char != '\\' and char != '/':
                continue

            if col_index == 0: # found at the start of the level
                if char == '/':
                    # |\
                    # |/
                    if level[col_index][row_index + 1] != '\\':
                        return False
                    elif level[col_index + 1][row_index] == '/':
                        # |\\
                        # |//
                        if level[col_index + 1][row_index+1] == '\\':
                            seen_indices.add((col_index, row_index))
                            seen_indices.add((col_index, row_index + 1))
                            seen_indices.add((col_index + 1, row_index))
                            seen_indices.add((col_index + 1, row_index + 1))
                        else:
                            return False
                    else:
                        seen_indices.add((col_index, row_index))
                        seen_indices.add((col_index, row_index + 1))
                else:
                    # |/\\
                    # |\//
                    if level[col_index][row_index + 1] != '/' and \
                       level[col_index + 1][row_index] != '/' and \
                       level[col_index + 1][row_index + 1] != '\\' and \
                       level[col_index + 2][row_index] != '/' and \
                       level[col_index + 2][row_index + 1] != '\\':
                        return False
                    elif level[col_index + 3][row_index] == '/':
                        # |//\\
                        # |\\//
                        if level[col_index + 3][row_index + 1] != '\\':
                            return False
                        else:
                            seen_indices.add((col_index, row_index))
                            seen_indices.add((col_index, row_index + 1))
                            seen_indices.add((col_index + 1, row_index))
                            seen_indices.add((col_index + 1, row_index + 1))
                            seen_indices.add((col_index + 2, row_index))
                            seen_indices.add((col_index + 2, row_index + 1))
                            seen_indices.add((col_index + 3, row_index))
                            seen_indices.add((col_index + 3, row_index + 1))
                    else:
                        seen_indices.add((col_index, row_index))
                        seen_indices.add((col_index, row_index + 1))
                        seen_indices.add((col_index + 1, row_index))
                        seen_indices.add((col_index + 1, row_index + 1))
                        seen_indices.add((col_index + 2, row_index))
                        seen_indices.add((col_index + 2, row_index + 1))
                        
            elif col_index == col_length - 1:
                # /|
                # \|
                if not __check(col_index, row_index + 1, level, '/', seen_indices):
                    return False
            elif col_index == col_length - 2:
                # //|
                # \\|
                if not __check(col_index, row_index + 1, level, '/', seen_indices) or \
                   not __check(col_index + 1, row_index, level, '\\', seen_indices) or \
                   not __check(col_index + 1, row_index + 1, level, '/', seen_indices):
                    return False
            elif col_index == col_length - 3:
                # //\|
                # \\/|
                if not __check(col_index, row_index + 1, level, '/', seen_indices) or \
                   not __check(col_index + 1, row_index, level, '\\', seen_indices) or \
                   not __check(col_index + 1, row_index + 1, level, '/', seen_indices) or \
                   not __check(col_index + 2, row_index, level, '/', seen_indices) or \
                   not __check(col_index + 2, row_index + 1, level, '\\', seen_indices):
                    return False
            else:
                # //\\
                # \\//
                if not __check(col_index, row_index + 1, level, '/', seen_indices) or \
                   not __check(col_index + 1, row_index, level, '\\', seen_indices) or \
                   not __check(col_index + 1, row_index + 1, level, '/', seen_indices) or \
                   not __check(col_index + 2, row_index, level, '/', seen_indices) or \
                   not __check(col_index + 2, row_index + 1, level, '\\', seen_indices) or \
                   not __check(col_index + 3, row_index, level, '/', seen_indices) or \
                   not __check(col_index + 3, row_index + 1, level, '\\', seen_indices):
                    return False
                
    return True


            