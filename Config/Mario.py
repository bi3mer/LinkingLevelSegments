from Game.Mario.IO import get_levels
from Game.Mario.Behavior import *
from Game.Mario.Fitness import *
from Utility import NGram
from Utility.LinkerGeneration import *

name = 'Mario'
data_dir = 'MarioData'

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

max_path_length = 5

def get_percent_playable(level, agent=None):
    return percent_playable(level)

def get_fitness(level, percent_playable, agent=None):
    bad_n_grams = gram.count_bad_n_grams(level)
    return bad_n_grams + 1 - percent_playable

fitness = lambda lvl: get_fitness(lvl, get_percent_playable(lvl))

def level_is_valid(level):
    # check for malformed pipes

    for col_index in range(len(level)):
        for row_index in range(len(level[0])):
            if level[col_index][row_index] == '[':
                if col_index + 1 >= len(level):
                    continue

                if level[col_index + 1][row_index] != ']':
                    return False

    return True