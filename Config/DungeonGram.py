from dungeongrams.dungeongrams import *
from Utility.DungeonGram.IO import get_levels
from Utility.DungeonGram.Behavior import *
from Utility import NGram
from Utility.GridTools import columns_into_rows
from Utility.LinkerGeneration import *

from dungeongrams import *

name = 'DungeonGrams'
data_dir = f'DungeonData'

fitness = lambda lvl: get_fitness(lvl, get_percent_playable(lvl))
is_vertical = False

n = 3
gram = NGram(n)
unigram = NGram(1)
levels = get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

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
