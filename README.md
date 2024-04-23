# TSPPH\_PerformanceAnalysis

This repository, like its submodule *TSPPartitionHeuristic*, is part of the "*Algorithms and Models for Discrete Optimization*" 2022/2023 course examination. The course is held at University of Rome, Tor Vergata.

Its focus is to test the performance of the *TSP Partition Heuristic* algorithm on various instances taken from TSP libraries found online, in order to check whether the heuristic can give useful solutions or not

# Layout of the repository

The definitive layout of the repository is yet to be defined, so  for the moment only an initial draft will be given:

  - TSPPartitionHeuristic : git submodule containing the heuristic's description and implementation

  - formatted\_instances : directory containing the library-compatible instances eventually converted from the online sources

  - resources : directory containing the instances files taken online

  - src : directory containing source code for the runners that generate the execution results of the algorithm

  - performance\_scripts : directory containing the script that generate the execution results of the algorithm

  - results : directory containing the results produced by instance processing

  - adapters : directory containing scripts written in order to transform the instances

  - analyzers : directory containing software for statistical processing of the results
  
  - extra : directory containing intermediate scripts used in the development process

# Building

The build system used by this project is `GNU Make`.
Here is a list of the targets that can be run

-
  ``` bash
    make convert
  ```

  to download the instances and convert them in a format readable from the _TSP Partition Heuristic_ library.

-
  ``` bash
    make performance_scripts_build
  ```

  to build the scripts that take the files generated from `make convert` and do performance evaluation on them.

  Note: to use the _HiGHS_ solver one of the following is needed :

  - Defining the environment variable `HIGHS_SOURCE_DIR` to the path in which the checkout command for _HiGHS_ has been run if there is a local build.

  - Defining the environment variable `HIGHS_INSTALL_DIR` to the path in which _HiGHS_ has been installed in case of a custom installation.

  - Install _HiGHS_ in your system (see [here](https://ergo-code.github.io/HiGHS/dev/installation/#Compile-from-source)).

- 
  ``` bash
    make non_relaxed_time_analysis_build
  ```

  to build the scripts that test your PC's ability to solve instances of a certain dimension, useful for configuring the algorithm threshold. Like above, _HiGHS_ or other solvers are needed.


# Credits

The evaluated instances are taken from the following source(s) :

  - [TSPLIB95 : Gerhard Reinelt Universität Heidelberg Institut für Angewandte Mathematik](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)

As for the tests in TSPPartitionHeuristic, the solver used for the performance evaluation is HiGHS, see :

- Parallelizing the dual revised simplex method Q. Huangfu and J. A. J. Hall Mathematical Programming Computation, 10 (1), 119-142, 2018. DOI: 10.1007/s12532-017-0130-5