from Config import Mario, Icarus, DungeonGram
import Pypy3_Tasks

from time import time
import argparse
import sys

start = time()

parser = argparse.ArgumentParser(description='Gram-Elites')
parser.add_argument('--seed', type=int, default=0, help='Set seed for generation')
parser.add_argument(
    '--runs', 
    type=int,
    default=10,
    help='Set the # of runs for --average-generated.')
parser.add_argument('--segments', type=int, default=3, help='set # of segments to be combined.')

game_group = parser.add_mutually_exclusive_group(required=True)
game_group.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
game_group.add_argument('--mario', action='store_true', help='Run Mario')
game_group.add_argument('--icarus', action='store_true', help='Run Icarus')

algorithm_group = parser.add_mutually_exclusive_group(required=True)
algorithm_group.add_argument('--n-gram-placement', action='store_true', help='N-Grams with placement into bins')
algorithm_group.add_argument('--map-elites', action='store_true', help='map-elites with standard operators')
algorithm_group.add_argument('--gram-elites', action='store_true', help='gram-elites')

task_group = parser.add_mutually_exclusive_group(required=True)
task_group.add_argument('--generate-corpus', action='store_true', help='Generate a corpus')
task_group.add_argument('--plot-map-elites', action='store_true', help='Build plots from data generated with --generate-corpus')
task_group.add_argument('--average-generated', action='store_true', help='Generate a set of corpuses to get the average # levels generated.')
task_group.add_argument('--plot-counts', action='store_true', help='Build count graph from data generated with --average-generated')

args = parser.parse_args()

if args.dungeongram:
    config = DungeonGram
elif args.mario:
    config = Mario
elif args.icarus:
    config = Icarus
else:
    parser.print_help(sys.stderr)
    sys.exit(-1)

if args.n_gram_placement:
    print('Algorithm => N-Grams with Placement')
    config.start_population_size += config.iterations
    config.iterations = 0
    alg_type = 'n_gram'
elif args.map_elites:
    print('Algorithm => MAP-Elites with standard operators and n-gram population generation')
    alg_type = 'map_elites'
elif args.gram_elites:
    print('Algorithm => Gram-elites')
    config.crossover = config.n_crossover
    config.mutate = config.n_mutate
    alg_type = 'gram_elites'
else:
    parser.print_help(sys.stderr)
    sys.exit(-1)

if args.generate_corpus:
    Pypy3_Tasks.GenerateCorpus(config, alg_type).run(args.seed)
elif args.average_generated:
    Pypy3_Tasks.AverageGenerated(config, alg_type, args.seed).run(args.runs)
elif args.plot_map_elites:
    import PlotTasks
    PlotTasks.MapElitesPlotter.run(config, alg_type)
elif args.plot_counts:
    import PlotTasks
    PlotTasks.AverageLevelsFoundPlotter.run(config, alg_type)
else:
    parser.print_help(sys.stderr)
    sys.exit(-1)

end = time()

hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

# mac only
import os
os.popen('say "Done!"')