from Config import Mario, Icarus, DungeonGram

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

algorithm_group = parser.add_mutually_exclusive_group(required='--generate-links' in sys.argv)
algorithm_group.add_argument('--n-gram-placement', action='store_true', help='Segments from N-Grams with placement into bins')
algorithm_group.add_argument('--map-elites', action='store_true', help='Segments from MAP-Elites with standard operators')
algorithm_group.add_argument('--gram-elites', action='store_true', help='Segments from Gram-Elites')

task_group = parser.add_mutually_exclusive_group(required=True)
task_group.add_argument('--train', action='store_true', help='Train a network for a game.')
task_group.add_argument('--generate-links', action='store_true', help='Build plots from data generated with --generate-corpus')

args = parser.parse_args()

if args.dungeongram:
    config = DungeonGram
elif args.mario:
    config = Mario
elif args.icarus:
    config = Icarus

if args.n_gram_placement:
    alg_type = 'n_gram'
elif args.map_elites:
    alg_type = 'map_elites'
elif args.gram_elites:
    alg_type = 'gram_elites'
else:
    alg_type = None

if args.train:
    pass
if args.generate_links:
    if alg_type == None:
        print('Segments from algorithm type must be specified.')
        sys.exit(-1)

    print('Generating links')
    

end = time()

hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

# mac only
import os
os.popen('say "Done!"')