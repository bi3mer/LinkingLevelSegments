#!/bin/bash

screen -dm bash -c "pypy3 main.py --generate-links --dungeongram --gram-elites --allow-empty-link"
screen -dm bash -c "pypy3 main.py --generate-links --dungeongram --gram-elites --no-empty-link"
# screen -dm bash -c "pypy3 main.py --generate-links --icarus --gram-elites --allow-empty-link"
# screen -dm bash -c "pypy3 main.py --generate-links --mario --gram-elites --allow-empty-link"
