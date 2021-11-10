import time
from typing import Callable

import pygame
from pygame.locals import *

from Box2D.b2 import *
from Box2D import *
import sys

# Internal modules import
from Car import Car
from Terrain import Terrain

import logging

from CustomFormatter import CustomFormatter

# Game parameters
# Maximum duration of a run (in seconds)
MAX_RUN_DURATION = 2 * 60  # run time in seconds
# Number of generations in one game
NUMBER_OF_GENERATIONS = 6

# colors for the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
BACKGROUND = (90, 23, 100, 100)
GRASS = (160, 96, 69, 255)
TERRAIN = (189, 123, 95, 255)
WHEELS_OUTER = (38, 192, 90)  # outer color for the wheels
WHEELS_INNER = (255, 0, 0)
DEAD = (125, 125, 125)
colors = {
    b2_staticBody:  GRASS,  # terrain
    b2_dynamicBody: (127, 127, 127, 255)   # car chassis
}

print(pygame.__file__)
pygame.init()

font_top = pygame.font.SysFont('Comic Sans MS', 16)  # used for the top 2..n cars i the end display

class Game:
    """
    A class that represents a game.
    """

    def __init__(self, next_generation: Callable, isDraw: bool, seed_terrain: int, seed_car: int, isLogged=True):
        """
        Initializes an object of class Game.
        :param next_generation: function that creates the new generation of cars, based on the previous one.
        """

        if isLogged:
            # Initialize logger
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(CustomFormatter())
            self.log = logging.getLogger('game')
            logging.basicConfig(level=logging.INFO)
            self.log.setLevel(logging.INFO)
            self.log.addHandler(ch)
            self.log.propagate = False
        else:
            self.log = logging.getLogger('game')

        # Set next generation function
        self.next_generation = next_generation

        self.score = 0.0
        self.current_time = 0
        self.world = b2World(gravity=(0, -9.81), doSleep=True)
        self.population_size = 20

        self.killed = 0
        self.seed_car = seed_car

        t = Terrain(self.world,seed_terrain)
        self.terrain = t.create_floor()

        self.population = []  # Array of Car objects
        self.create_first_generation()
        self.leader_coors = [0, 0]
        self.leader = self.population[0]  # 1st car

        self.isDraw = isDraw

        self.draw_any()

    def draw_any(self) -> None:
        """
        Draws the GUI of the game.
        """

        PPM = 30.0  # pixels per meter
        TARGET_FPS = 60
        TIME_STEP = 1.0 / TARGET_FPS
        SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
        SCORES_WIDTH, BORDER = font_top.size("Top 5: 9999.9 m")  # where the scores will be written
        INIT_SCORE_WIDTH, _ = font_top.size("Current: 9999.9 m ")  # where the scores will be written
        running = True
        
        screen = None
        if self.isDraw:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BORDER), 0, 32)
            pygame.display.set_caption('INGI-Dakar 2k21')
        else:
            screen = pygame.display.set_mode((1,1))
            #pygame.display.flip()

        clock = pygame.time.Clock()

        def my_draw_circle(circle, body, fixture) -> None:
            """
            Draws a circle shape.
            """
            position = body.transform * circle.pos * PPM

            y_offset = ((self.leader.chassis.body.worldCenter.y) * 70)
            if y_offset < -300:
                y_offset = -300
            if y_offset > 300:
                y_offset = 300

            position = (
            position[0] - self.leader.chassis.body.worldCenter.x * 30 + 350, SCREEN_HEIGHT - position[1] + y_offset * 0.5 - 200)

            center_s = [int(circle.radius * PPM),
                        int(circle.radius * PPM)]  # this is for drawing on the new surface we create below
            # 0,0 is top left corner, so to draw a circle on the top
            # left corner, we set center as radius,radius

            s = pygame.Surface(
                (50, 50))  # create a surface just enough for the wheel radius , too big will cause the sim. to lag
            s.set_alpha(100)  # transparancy value
            s.fill(WHITE)  # fill the screen
            s.set_colorkey(WHITE)  # comment this to see how screen blit works

            pygame.draw.circle(s, WHEELS_OUTER, center_s, int(circle.radius * PPM),0)  # draw a circle on the new screen we created

            t = body.transform
            axis = b2Mul(t.q, b2Vec2(10.0, 25.0))

            pygame.draw.aaline(s, WHEELS_INNER, center_s,
                               (center_s[0] - circle.radius * axis[0], center_s[1] + circle.radius * axis[1]))

            screen.blit(s, (position[0] - int(circle.radius * PPM), position[1] - int(circle.radius * PPM)))

        b2CircleShape.draw = my_draw_circle

        def my_draw_polygon(polygon, body, fixture) -> None:
            """
            Draws a polygon shape.
            """
            y_offset = ((self.leader.chassis.body.worldCenter.y) * 70)
            if y_offset < -300:
                y_offset = -300
            if y_offset > 300:
                y_offset = 300
            vertices = [(body.transform * v) * PPM for v in polygon.vertices]
            vertices = [(v[0] - self.leader.chassis.body.worldCenter.x * 30 + 350, SCREEN_HEIGHT - v[1] + y_offset * 0.5 - 200) for v
                        in vertices]
            if body.type == b2_staticBody:  # draw area under the polygon if it was a static body, to display terrain
                inf = float("inf")
                minX = inf
                maxX = -inf
                left_bot = (inf, -inf)
                right_bot = (-inf, -inf)
                for vert in vertices:
                    x, y = vert[0], vert[1]
                    if minX >= x:
                        minX = x
                        left_bot = (x, y) if y > left_bot[1] or left_bot[0] > x else left_bot
                    if maxX <= x:
                        maxX = x
                        right_bot = (x, y) if y > right_bot[1] or right_bot[0] < x else right_bot
                points = [left_bot, (minX, SCREEN_HEIGHT), (maxX, SCREEN_HEIGHT), right_bot]
                pygame.draw.polygon(screen, TERRAIN, points)
            pygame.draw.polygon(screen, colors[body.type], vertices)

        def draw_top_scores(n: int = 5):
            """
            draw the top current distances of several carson the screen
            :return: None
            """
            top_scores = sorted([car.max_dist for car in self.population], reverse=True)[:n]
            # draw a black rectangle
            pygame.draw.rect(screen, BLACK, pygame.Rect(0, SCREEN_HEIGHT, SCREEN_WIDTH, BORDER))
            # draw the description for the current car
            description = f"Current: {self.leader.max_dist:.1f} m"
            text_surface = font_top.render(description, True, WHITE)
            screen.blit(text_surface, (0, SCREEN_HEIGHT))

            for i, score in enumerate(top_scores):  # write the top distances on the rectangle
                description = f"Top {i+1}: {score:.1f} m"
                maxX = INIT_SCORE_WIDTH + i * SCORES_WIDTH + font_top.size(description)[1]
                if maxX > SCREEN_WIDTH:
                    break
                text_surface = font_top.render(description, True, WHITE)
                screen.blit(text_surface, (INIT_SCORE_WIDTH + i * SCORES_WIDTH, SCREEN_HEIGHT))


        polygonShape.draw = my_draw_polygon  # modify the drawing for the corresponding polygon

        generation = 0
        self.log.info("Generation n°" + str(generation+1))
        max_time = time.time() + MAX_RUN_DURATION
        current_time = time.time()
        bg = pygame.image.load("../asset/background.png")
        while running and generation < NUMBER_OF_GENERATIONS:
            self.update_car_data()
            self.update_leader()
            if self.killed == self.population_size or current_time > max_time:
                generation_score = 0
                for i in range(len(self.population)):
                    if self.population[i].max_dist > generation_score:
                        generation_score = self.population[i].max_dist
                    if self.population[i].max_dist > self.score:
                        self.score = self.population[i].max_dist
                self.log.info("Generation n°" + str(generation + 1) + " score: " + str(generation_score))
                self.population = self.next_generation(self.world, self.population)
                self.killed = 0
                generation += 1
                if generation < NUMBER_OF_GENERATIONS:
                    self.log.info("Generation n°" + str(generation + 1))
                max_time = time.time() + MAX_RUN_DURATION
                current_time = time.time()
            # Check the event queue
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    # The user closed the window or pressed escape
                    running = False
                    sys.exit()  # quit the game

            if self.isDraw:
                # screen.fill(BACKGROUND)
                screen.blit(bg, (0, 0))
                # 229,153,153,255
                # Draw the world
                for body in self.world.bodies:
                    for fixture in body.fixtures:
                        fixture.shape.draw(body, fixture)
            # draw the scores
            draw_top_scores()

            # Make Box2D simulate the physics of our world for one step.
            self.world.Step(TIME_STEP, 10, 10)

            if self.isDraw:
                # Flip the screen and try to keep at the target FPS
                pygame.display.flip()
                clock.tick(TARGET_FPS)

    def update_leader(self) -> None:
        """
        Updates the Car that is centered on the game GUI.
        :return:
        """
        sorted_data = sorted(self.population, key=lambda x: x.max_dist)
        for data in sorted_data:
            if not data.isDead:
                self.leader = data

    def Step(self, settings) -> None:
        """
        Advances one step in the world simulation of the game>=.
        :param settings: game configuration
        """
        super(Game, self).Step(settings)

        self.update_car_data()

        if self.killed == self.population_size:
            self.population = self.next_generation(self.world, self.population)

    def start(self) -> None:
        """
        Starts the world simulation of the game.
        """
        while True:
            self.update_car_data()
            if self.killed == self.population_size:
                self.population = self.next_generation(self.world, self.population)

    def update_car_data(self) -> None:
        """
        Updates the state of each Car in the game.
        :return:
        """
        for index, car in enumerate(self.population):
            if not car.isDead:
                car.set_pos_and_vel([self.population[index].chassis.body.position.x, self.population[index].chassis.body.position.y],
                                     self.population[index].chassis.body.linearVelocity.x)
                if car.isDead:
                    # id you want to keep all the cars on the screen, (only for testing) commend the bottom 5 lines
                    for wheel in self.population[index].wheels:
                        if wheel:
                            self.world.DestroyBody(wheel.body)  # remove wheels
                    self.world.DestroyBody(self.population[index].chassis.body)  # remove chassis
                    #self.population[index] = None
                    self.killed += 1  # turn this on only after all the mate,mutate methods work
                    self.log.info("killed so far: " + str(self.killed))

    def sort_by_dist(self) -> None:
        """
        Sorts the population of Cars by their maximum distance reached.
        """
        self.population = sorted(self.population, key=lambda x: x.max_dist)
        self.leader_coors = [self.population[0].chassis.body.worldCenter.x,
                             self.population[0].chassis.body.worldCenter.y]
        self.leader = self.population[0]

    def create_first_generation(self) -> None:
        """
        Creates the first Car population, which is a population with random attributes.
        """
        for i in range(self.population_size):
            self.population.append(Car.create_random_car(self.world,self.seed_car,i))
