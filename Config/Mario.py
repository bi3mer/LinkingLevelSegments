from Optimization.Operators import *
from Utility.Mario.IO import get_levels
from Utility.Mario.Behavior import *
from Utility.Mario.Fitness import *
from Utility import NGram
from Utility.LinkerGeneration import *

from os.path import join

name = 'Mario'

data_dir = 'MarioData'

flawed_agents = [
    'NO_ENEMY',
    'NO_HIGH_JUMP',
    'NO_JUMP',
    'NO_SPEED'
]

start_population_size = 500
iterations = 80_000

feature_names = ['linearity', 'leniency']
feature_descriptors = [percent_linearity, percent_leniency]
feature_dimensions = [[0, 1], [0, 1]] 

elites_per_bin = 4
resolution = 40

uses_separate_simulation = False
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

minimize_performance = True

start_strand_size = 25
max_strand_size = 25

mutation_values = list(unigram_keys)
mutate = Mutate(mutation_values, 0.02)
crossover = SinglePointCrossover()

n_mutate = NGramMutate(0.02, gram, max_strand_size)
n_crossover = NGramCrossover(gram, start_strand_size, max_strand_size)
population_generator = NGramPopulationGenerator(gram, start_strand_size)

x_label = 'Linearity'
y_label = 'Leniency'
title = ''

max_path_length = 5

def get_percent_playable(level, agent=None):
    return percent_playable(level)

def get_fitness(level, percent_playable, agent=None):
    bad_n_grams = gram.count_bad_n_grams(level)
    return bad_n_grams + 1 - percent_playable

fitness = lambda lvl: get_fitness(lvl, get_percent_playable(lvl))

