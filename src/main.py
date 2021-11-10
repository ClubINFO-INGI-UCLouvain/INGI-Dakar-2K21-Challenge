from time import sleep
from typing import List
from Game import Game
from Car import Car
from Box2D import b2World
import logging
from CustomFormatter import CustomFormatter
import matplotlib.pyplot as plt
import argparse
import sys

# Number of games played
# The final score is computed by averaging the scores of all the games
number_of_games = 5

# Logger
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
log = logging.getLogger('main')
logging.basicConfig(level=logging.INFO)
log.setLevel(logging.INFO)
log.addHandler(ch)
log.propagate = False


def parse_arguments():
    show_plot = True
    isDraw = True
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no_UI",
        help="Disable UI (default: UI enable)",
        action="store_false",
    )
    parser.add_argument(
        "--no_plot",
        help="Disable UI (default: Plot enable)",
        action="store_false",
    )
    parser.add_argument(
        "--seed_terrain",
        help="Seed for the terrain (default: 42)",
        type=int,
        default=42,
    )
    parser.add_argument(
        "--seed_car",
        help="Seed for the car (default: 666)",
        type=int,
        default=666,
    )
    parser.add_argument(
        "--easter",
        help="Mystery",
        action="store_true",
    )
    args = parser.parse_args()
    if args.easter:
        log.info("\(*o*)/ Christophe is God \(*_*)/")
    if not args.no_UI:
        isDraw = False
    if not args.no_plot:
        show_plot = False
    return isDraw, show_plot, args.seed_terrain, args.seed_car
        

def next_generation(world: b2World, population: List[Car]) -> List[Car]:
    """
    TODO by student
    This function is the one you have to implement for the contest.
    It must produce a next generation of Car objects,
    by applying the concepts of genetic algorithms on the previous generation.
    :param world: b2World that represents the world where the game is simulated
    :param population: the previous Car population
    :return: the next generation of Car objects
    """
    # Default implementation: the new generation is the same as the previous one
    new_population = []
    for car in population:
        new_population.append(Car(world, car.wheel_radius, car.wheel_vertex, car.motor_wheel_index, car.chassis_vertex))
    return new_population


# Run games and compute final score
if __name__ == "__main__":
    isDraw, show_plot, seed_terrain, seed_car = parse_arguments()
    games = []
    scores = []
    sum_scores = 0
    for i in range(number_of_games):
        log.info("\n"+"-"*20 + "\nGame n°" + str(i+1) + "\n" + "-"*20)
        isLogged = True if i == 0 else False
        game = Game(next_generation, isDraw, seed_terrain, seed_car, isLogged)
        games.append(i + 1)
        scores.append(game.score)
        sum_scores += game.score
        log.info("Game n°" + str(i + 1) + " score: " + str(game.score))

    # Final score is the average of each run's score
    final_score = sum_scores / number_of_games
    log.info("\n"+"-"*20 + "\nEnd of the game" + "\n" + "-"*20)
    log.info("Your final score is {}".format(final_score))
    if show_plot:  # To get time to see the plot
        plot = plt.figure(1)
        plt.xlabel("Game")
        plt.ylabel("Best car score")
        plt.bar(games, scores)
        plt.show()
        '''
        while True:
            try:
                log.info("Send SIGINT to finish the game (CTRL + C)")
                sleep(10)
            except KeyboardInterrupt:
                sys.exit() 
        '''