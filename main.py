from Config import Mario, Icarus, DungeonGram
from Pypy3_Tasks import *

from time import time
import argparse
import sys

from Pypy3_Tasks import DEBUG_build_link

start = time()

parser = argparse.ArgumentParser(description='Linking Level Segments')
parser.add_argument('--seed', type=int, default=0, help='Set seed for generation')
parser.add_argument(
    '--runs', 
    type=int,
    default=10,
    help='Set the # of runs for --average-generated.')
parser.add_argument('--src', type=str, default='0_0_0.txt', help='source segment linked with --debug-build-link and --debug-view-link')
parser.add_argument('--tgt', type=str, default='0_0_0.txt', help='source segment linked with --debug-build-link and --debug-view-link')

empty_link_group = parser.add_mutually_exclusive_group(required=True)
empty_link_group.add_argument('--allow-empty-link', action='store_true', help='Allow links to be empty')
empty_link_group.add_argument('--no-empty-link', action='store_true', help='Allow links to be empty')

game_group = parser.add_mutually_exclusive_group(required=True)
game_group.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
game_group.add_argument('--mario', action='store_true', help='Run Mario')
game_group.add_argument('--icarus', action='store_true', help='Run Icarus')

arg_exists = any(['--generate-links' in sys.argv, '--debug-segments-are-valid' in sys.argv])
algorithm_group = parser.add_mutually_exclusive_group(required=arg_exists)
algorithm_group.add_argument('--n-gram-placement', action='store_true', help='Segments from N-Grams with placement into bins')
algorithm_group.add_argument('--map-elites', action='store_true', help='Segments from MAP-Elites with standard operators')
algorithm_group.add_argument('--gram-elites', action='store_true', help='Segments from Gram-Elites')

task_group = parser.add_mutually_exclusive_group(required=True)
task_group.add_argument('--generate-links', action='store_true', help='Build plots from data generated in GramElitesData')
task_group.add_argument('--test-links', action='store_true', help='Test all links built with --generate-links')
task_group.add_argument('--link-stats', action='store_true', help='Get stats of links built with --generate-links')
task_group.add_argument('--walkthrough', action='store_true', help='Run walkthrough.')
task_group.add_argument('--walkthrough-stats', action='store_true', help='Get stats from --walkthrough run')
task_group.add_argument('--debug-build-link', action='store_true', help='DEBUG that building a link between two training levels works')
task_group.add_argument('--debug-segments-are-valid', action='store_true', help='DEBUG that all segments in GramElitesData are valid for an [alg-type]')
task_group.add_argument('--debug-test-levels', action='store_true', help='DEBUG test levels in the test_levels directory for level_is_valid')
task_group.add_argument('--debug-view-link', action='store_true', help='view a link between two segments')

args = parser.parse_args()

if args.dungeongram:
    config = DungeonGram
elif args.mario:
    config = Mario
elif args.icarus:
    config = Icarus

if args.allow_empty_link:
    config.ALLOW_EMPTY_LINK = True
else:
    config.ALLOW_EMPTY_LINK = False

if args.n_gram_placement:
    alg_type = 'n_gram'
elif args.map_elites:
    alg_type = 'map_elites'
elif args.gram_elites:
    alg_type = 'gram_elites'
else:
    alg_type = None

if args.generate_links:
    if alg_type == None:
        print('Segments from algorithm type must be specified.')
        sys.exit(-1)

    GenerateLinks(config, alg_type, args.seed).run()
elif args.test_links:
    TestLinks(config, alg_type, args.seed).run()
elif args.link_stats:
    LinkStats(config, alg_type, args.seed).run()
elif args.walkthrough:
    Walkthrough(config, alg_type, args.seed).run()
elif args.walkthrough_stats:
    WalkthroughStats(config, alg_type, args.seed).run()
elif args.debug_build_link:
    DEBUG_build_link(config, alg_type, args.seed).run(args.src, args.tgt)
elif args.debug_segments_are_valid:
    DEBUG_segments_are_valid(config, alg_type, args.seed).run()
elif args.debug_test_levels:
    DEBUG_test_levels(config, alg_type).run()
elif args.debug_view_link:
    DEBUG_view_link(config, alg_type).run(args.src, args.tgt)

end = time()

hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

# mac only
import os
os.popen('say "Done!"')