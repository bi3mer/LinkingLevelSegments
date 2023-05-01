# On Linking Level Segments

## Abstract 

An increasingly common area of study in procedural content generation is the creation of level segments: short pieces that can be used to form larger levels. Previous work has used basic concatenation to form these larger levels. However, even if the segments themselves are completable and well-formed, concatenation can fail to produce levels that are completable and can cause broken in-game structures (e.g. malformed pipes in \textit{Mario}). We show this with three tile-based games: a side-scrolling platformer, a vertical platformer, and a top-down roguelike. Additionally, we present a Markov chain and a tree search algorithm that finds a link between two level segments, which uses filters to ensure completability and unbroken in-game structures in the linked segments. We further show that these links work well for multi-segment levels. We find that this method reliably finds links between segments and is customizable to meet a designer’s needs.

## Use

I highly recommend using [PyPy3](https://www.pypy.org/) else everything below could take a while to run.

- *Set game to run:* {GAME} => [--dungeongram, --mario, --icarus]
- *Set whether links can be empty or not:* {LINK} => [--allow-empty-link, --no-empty-link]
- By default, everything uses the [gram-elites](https://dl.acm.org/doi/abs/10.1145/3472538.3472599) dataset but others could be used.

#### Generate Links

```
pypy3 main.py --generate-links --{GAME} --gram-elites --{ALLOW_LINK}
```

#### Test Links

```
pypy3 main.py --test-links --{GAME} --gram-elites --{ALLOW_LINK}
```

#### Get Stats for Links

```
pypy3 main.py --link-stats --{GAME} --gram-elites --{ALLOW_LINK}
```

#### Walkthrough Links 

```
pypy3 main.py --walkthrough --{GAME} --gram-elites --{ALLOW_LINK} --runs 1000
```

#### Stats from Walkthrough

```
pypy3 main.py --walkthrough-stats --{GAME} --gram-elites --{ALLOW_LINK} --runs 1000
```

#### Other
I also have multiple debugging tools that you can use. 

```
pypy3 main.py --help
```

## Citation 

```
@inproceedings{biemer2022linking,
  title={On Linking Level Segments},
  author={Biemer, Colan F and Cooper, Seth},
  booktitle={2022 IEEE Conference on Games (CoG)},
  pages={199--205},
  year={2022},
  organization={IEEE}
}
```
