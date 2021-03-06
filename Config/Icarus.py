from Utility.StructureChain import StructureChain
from dungeongrams.dungeongrams import *
from Game.Icarus.IO import get_levels, level_to_str
from Game.Icarus.Behavior import *
from Game.Icarus.Fitness import *
from Utility import NGram, Ngram
from Utility.LinkerGeneration import *
from dungeongrams import *

name = 'Icarus'
data_dir = 'IcarusData'

resolution = 40

link_distance_dependent = False
def lines_to_level(lines):
    return[l.strip() for l in reversed(lines)]


BETWEEN_LINK_TOKEN = '                '
n = 2
gram = NGram(n)
unigram = NGram(1)
FORWARD_STRUCTURE_GRAM = StructureChain(['d', 'D'], 2)
BACKWARD_STRUCTURE_GRAM = StructureChain(['d', 'D'], 2, backward=True)
LEVELS = get_levels(lines_to_level)

for level in LEVELS:
    gram.add_sequence(level)
    unigram.add_sequence(level)

    FORWARD_STRUCTURE_GRAM.add_sequence(level)
    BACKWARD_STRUCTURE_GRAM.add_sequence(level)

ELITES_PER_BIN = 4

unigram_keys = set(unigram.grammar[()].keys())
pruned = gram.fully_connect() # remove dead ends from grammar
unigram_keys.difference_update(pruned) # remove any n-gram dead ends from unigram

LINKERS = [
    ['---XXXX--XXXX---'],
    ['XXX----XX----XXX'],
    ['----------------'],
]
ALLOW_EMPTY_LINK = True
MAX_LINK_LENGTH = 7

FEATURE_NAMES = ['density', 'leniency']
FEATURE_DESCRIPTORS = [density, leniency]

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
            if row_index == 0 and current_char == 'd':
                seen.add((row_index, col_index))
            
            # case 2: door is incomplete at end ------D|d
            elif row_index == len(level) - 1: 
                if current_char == 'D':
                    seen.add((row_index, col_index)) # technically not necessary
            
            # Case 3: door is full, Dd
            elif current_char == 'D' and level[row_index + 1][col_index] == 'd':
                seen.add((row_index, col_index))
                seen.add((row_index + 1, col_index))
            else:
                return False

    return True

# def all_structures_complete(level):
#     num_columns = len(level[0])
#     seen = set()
#     for row_index in range(len(level)):
#         for col_index in range(num_columns):
#             current_char = level[row_index][col_index]
#             if current_char != 'D' and current_char != 'd':
#                 continue

#             if (row_index, col_index) in seen:
#                 continue

#             # Case 3: door is full, Dd
#             if current_char == 'D' and level[row_index + 1][col_index] == 'd':
#                 seen.add((row_index, col_index))
#                 seen.add((row_index + 1, col_index))
#             else:
#                 return False

#     return True