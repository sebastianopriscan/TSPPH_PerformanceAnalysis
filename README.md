# TSPPH\_PerformanceAnalysis

This repository, like its submodule *TSPPartitionHeuristic*, is part of the "*Algorithms and Models for Discrete Optimization*" 2022/2023 course examination. The course is held at University of Rome, Tor Vergata.

Its focus is to test the performance of the *TSP Partition Heuristic* algorithm on various instances taken from TSP libraries found online, in order to check whether the heuristic can give useful solutions or not

# Layout of the repository

The definitive layout of the repository is yet to be defined, so  for the moment only an initial draft will be given:

  - TSPPartitionHeuristic : git submodule containing the heuristic's description and implementation

  - formatted\_instances : directory containing the library-compatible instances eventually converted from the online sources

  - resources : directory containing the instances files taken online

  - results : directory containing the results produced by instance processing

  - adapters : directory containing scripts written in order to transform the instances

  - analyzers : directory containing software for statistical processing of the results
  
  - extra : directory containing intermediate scripts used in the development process

# Building

For the moment, run

``` bash
  make convert
```

to download the instances and convert them in a format readable from the _TSP Partition Heuristic_ library.

# Credits

The evaluated instances are taken from the following source(s) :

  - [TSPLIB95 : Gerhard Reinelt Universität Heidelberg Institut für Angewandte Mathematik](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)
