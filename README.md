# :car: INGI Dakar 2K21 - Be the first one on the finish line ! :car:

This year's first semester Club Info challenge will put you at the head of a car racing team.
You will participate to the world's most famous racing contest, the INGI Dakar.
Your goal is to build the best car, and to beat your opponents by reaching the furthest distance from the starting line.

## Challenge statement

Each group will be put in charge of a car racing team.
Ultimately, your goal is to reach the furthest distance from the starting line, with any of your cars.
For this, you will have 6 generations of 20 cars.
Each generation will be produced based on the previous one.
Your job is thus to implement the algorithm that takes the previous generation of cars in argument,
and that produces the next generation.
Such an algorithm is called a **genetic algorithm**, for which a theoretical background is given hereafter.

### Genetic algorithms

Genetic algorithms (GA) are inspired by the process of natural selection. They are used to resolve complex problems. They use operators such as mutation, crossover and selection. GA process is split into generations. Each generation is composed of a finite number of individuals which are built from the best individuals of the last generation and one or several operators. The first generation is generally randomly created.

Genetic algorithms are used for a large variety of problems from antenna shape optimization to minimize the weight of structures embarked in mars rovers.

A genetic algorithm is based on three operators:

- Mutation, a mutation is a random modification of a parameter for an individual in the generation,
- Crossover, a crossover is the creation of an individual based on parameters values from several members of the last generation,
- Selection, in a genetic algorithm, we select the best individuals of a generation to construct the next generation.

![Alternative text describing the image](https://www.tutorialspoint.com/genetic_algorithms/images/ga_motivation.jpg)

The Mutation operator is used to ensure that the selection is not trapped in a local optima and can not reach the global optima for each parameters.

Some useful links:
- [Theory of genetic algorithms](https://reader.elsevier.com/reader/sd/pii/S0304397500004060?token=6240AF810A6BC428879CE8AEB4F04F4AA5A72A2D98CAB426176300A0225D41DE6039B263D1BE7B53E6BCA3974706F28F&originRegion=eu-west-1&originCreation=20211107165130)
- [List of genetic algorithms application](https://en.wikipedia.org/wiki/List_of_genetic_algorithm_applications)
### Program specifications

The program for the INGI Dakar 2K21 is composed of 7 Python modules:
- `Car.py`: Defines the class `Car` that represents a car of the game.
A `Car` is composed of two `Wheel`s and a `Chassis`,
where the `Wheel`s are located on two of the four `Chassis` vertices.
- `Chassis.py`: Defines the class `Chassis` that represents a car chassis.
A `Chassis` is represented by four vertices connected with each other in a quadrilateral shape.
- `CustomFormatter.py`: Used for logging purposes.
- `Game.py`: Defines the class `Game` that represents a game of INGI Dakar 2K21,
i.e. the simulation of the 6 generations of 20 cars.
- `main.py`: Entry point of INGI Dakar 2K21, which launches the simulations and computes the score.
- `Terrain.py`: Defines the class `Terrain` that represents the terrain on which the cars are driving.
- `Wheel.py`: Defines the class `Wheel` that represents a car's wheel.
A `Wheel` is defined by its radius and the fact that it is a motor wheel or not.

To participate to the challenge, you only have to modify the function `next_generation` in the module `main.py`,
that takes a representation of the game world (a `b2World` object)
and the previous generation of cars (a list of `Car` objects) as arguments,
and that returns the next generation of cars (also a list of `Car` objects).
The car features that you can update for the next generation are given below.

### Car features

A car is composed of the following (the numbers in bold cannot be changed):
- **TWO** wheels, one of which is a motor wheel
- A chassis, composed by **FOUR** vertices, linked together to form a polygon shape.

The car features that you can modify to reach the maximum distance are the following:
- Radius of the two wheels, separately.
- Which wheel is the motor wheel.
- Position of the four vertices of the chassis.
- To which of the chassis' vertices the two wheels are attached.

Please consult the corresponding classes to understand how those features are expressed and used in the program.

### Score computation

To start the simulation of the challenge, just run the `python3 main.py` Python module. You must also activate the python virtual environment with `source penv/bin/activate`.

The execution of the challenge, and computation of your final score, is as follows:
- Each generation contains 20 cars. The maximum distance reached by any of the cars is recorded as
the score of this generation.
- A game is composed of 6 generations. The score of a game is the maximum score among all the generations.
- To smoothen the results, 5 games are launched after each other.
Your final score is the average of the different score you obtained during the games.

At the end of the 5 games, a plot will be shown, with your results for the 5 games.


## Installation and execution

### Installation

To install the project, first clone the repository with the following command:
```shell
git clone https://github.com/ClubINFO-INGI-UCLouvain/INGI-Dakar-2K21-Challenge.git
```

Then, install the needed libraries by running the `install.sh` script,
inside the project directory:
```shell
python3 -m venv penv;
source  penv/bin/activate;
chmod +x install.sh;
./install.sh;
```

### Execution

To run the challenge simulation, you can simply run the `main.py` Python module in the `src` directory,
with the following command:

```shell
cd src/
python3 main.py [--seed_terrain SEED] [--seed_car SEED] [--no_UI] [--no_plot]
```

The command line arguments, all optional, are the following:
- `--seed_terrain SEED` (with `SEED` an integer): sets the seed for the random generation of the game terrain to `SEED`,
for reproducibility of the simulations
- `--seed_car SEED` (with `SEED` an integer): sets the seed for the random generation
of the first generation of cars to `SEED`, for reproducibility of the simulations
- `--no_UI`: does not show the graphical interface of the game, which drastically speeds up the simulations
- `--no_plot`: does not show the plot of the games' result at the end of all the games

Note that, for the contest, the seeds will be fixed for equity among the groups.

There is also a hidden argument, maybe you can try to find it :wink:
