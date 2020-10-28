# Implementation of NEAT
This repository implements the NEAT algorithm developed by Kenneth O. Stanley and Risto Miikkulainen from the University of Texas. There are 3 main parts in the repository.

## Part 1: visualistion_lab.py ##
This module uses Pygame to allow visualisation of the performance of the network in various scenarios. The default version visualises a gatherer learning optimum resource acquirement.

## Part 2: neural_netwrok_lab.py ##
This is the core of the project. Implementation of NEAT.

## Part 3: integrate_lab.py ##
**The main module to be run.** Combines Part 1 and Part 2. Sets the problems/rules (initial configuration) for the neural network to find the optimal solution.

For general case where you need to tune the parameters, you should refer to Part 3 on how to integrate the module with your code.

Video demonstration of Generation 227 and Generation 228:

https://drive.google.com/file/d/1poSh1_VAPzkwVnQ3ImqzWIEQbBY8FGRh/view?usp=sharing

## Applications ##
Repositries using this implementation:

1. https://github.com/jeqinchooi/Stereophonic-hearing
