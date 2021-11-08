from dungeongrams.dungeongrams import *
from Game.Icarus.IO import get_levels
from Game.Icarus.Behavior import *
from Game.Icarus.Fitness import *
from Utility import NGram
from Utility.LinkerGeneration import *
from dungeongrams import *

name = 'Icarus'
data_dir = 'IcrauData'

resolution = 40

n = 2
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
fitness = lambda level: get_fitness(level, get_percent_playable(level))
is_vertical = True

max_path_length = 4

__percent_completable = build_slow_fitness_function(gram)
def get_percent_playable(level, agent=None):
    return __percent_completable(level)

def get_fitness(level, percent_playable, agent=None):
    bad_n_grams = gram.count_bad_n_grams(level)
    return bad_n_grams + 1 - percent_playable

def filter(level):
    pass
