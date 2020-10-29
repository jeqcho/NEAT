# NEAT Implementation
This Python project implements the NEAT algorithm developed by Kenneth O. Stanley and Risto Miikkulainen from the University of Texas. NeuroEvolution of Augmenting Topologies (NEAT) is a genetic algorithm (GA) for the generation of evolving artificial neural networks (a neuroevolution technique). On simple control tasks, the NEAT algorithm often arrives at effective networks more quickly than other contemporary neuro-evolutionary techniques and reinforcement learning methods.

The project also provides visualisation of the best performing network in each generation, here is a snapshot of the visualisation program in work:
![NEAT snapshot](https://chojeq.com/home/img/NEAT.png)

Here is a video demonstration of Generation 227 and Generation 228:
![NEAT demonstration](https://drive.google.com/file/d/1poSh1_VAPzkwVnQ3ImqzWIEQbBY8FGRh/view?usp=sharing)


## Getting Started

Download all the Python files.
You should only run integrate_lab.py which is the main file of the program. It is also the file you should edit for tweaking the input and output parameters.

### Prerequisites

External python modules used are
```
import random
import copy
import pygame
import math
```

### Installing

After downloading the files, you can take a look at the integrate_lab.py file. These can be set by the user to experiment with different variables.

1. Download all Python files.
2. Run integrate_lab.py to check if the program is running smoothly.
3. After a training of the networks,  a report of statistics and animation of the best network will be played.
4. After the animation, the program will automatically proceed to train the next generation.
5. Stop the program.

Then, you should change some of the variables in integrate_lab.py. For example,

1. Change the population_limit to 50.
2. Run integrate_lab.py.
3. Review if changes are present during the reports after the network training. The field "Current population" should be 30.
4. Stop the program.


## Contributing

You can email me at chooijqweb@gmail.com regarding the future of this project.

## Versioning

Currently, the project is in version 11.0.
See the [version-history.txt](version-history.txt) file for details

## Applications

1. [Stereophonic hearing](https://github.com/jeqinchooi/Stereophonic-hearing)
Please e-mail me to add your project to the list if you are applying this implementation. Also, it is greatly appreciated if you cite this implementation in your project.

## Authors

* **Chooi Je Qin** - *Initial work* - [NEAT](https://github.com/jeqinchooi/NEAT)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This program implements the NEAT algorithm developed by Kenneth O. Stanley and Risto Miikkulainen from the University of Texas. You can read their paper [here](http://nn.cs.utexas.edu/downloads/papers/stanley.gecco02_1.pdf).
