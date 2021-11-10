# Import modules
from typing import List
from Wheel import Wheel
from Chassis import Chassis
from Box2D import b2RevoluteJointDef, b2Vec2, b2World
import random
import logging
from CustomFormatter import CustomFormatter


class Car:
    """
    A class that represent a Car.
    A Car is composed by a Chassis and two Wheels.
    """

    # Default Car values
    start_position = b2Vec2(1, 2)
    max_health = 100
    motorSpeed = 25

    def __init__(self, world: b2World, wheel_radius: List[float], wheel_vertex: List[int], motor_wheel_index: int, chassis_vertex: List[b2Vec2]):
        """
        Initializes an object of class Car.
        :param world: b2World where the Car will be used
        :param wheel_radius: list of the wheel radiuses
        :param wheel_vertex: list of the chassis vertices to which the wheels will be attached
        :param motor_wheel_index: index corresponding to the motor wheel
        :param chassis_vertex: list of the chassis vertices
        """

        # Create logger
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(CustomFormatter())
        self.log = logging.getLogger('car')
        logging.basicConfig(level=logging.INFO)
        self.log.setLevel(logging.INFO)
        self.log.addHandler(ch)
        self.log.propagate = False

        assert len(wheel_radius) == 2, "A car can only have 2 wheels"
        assert len(wheel_vertex) == 2, "A car can only have 2 wheels"
        assert 0 <= motor_wheel_index < len(wheel_radius), "The motor wheel index must be valid"
        self.wheel_count = len(wheel_radius)
        self.wheel_radius = wheel_radius
        self.wheel_vertex = wheel_vertex
        self.motor_wheel_index = motor_wheel_index

        self.alive = True
        self.velocityIndex = 0
        self.chassis_vertex = chassis_vertex
        self.chassis = Chassis(world, chassis_vertex, Car.start_position)
        self.wheels = []
        for i in range(self.wheel_count):
            self.wheels.append(Wheel(world, wheel_radius[i], Car.start_position))

        # Compute mass
        mass = self.chassis.body.mass
        for wheel in self.wheels:
            mass += wheel.body.mass

        # Compute torque
        self.torque = [mass * -world.gravity.y / radius for radius in wheel_radius]

        self.joint_def = b2RevoluteJointDef()
        for i in range(self.wheel_count):
            randvertex = self.chassis.vertex_list[self.wheel_vertex[i]]
            self.joint_def.localAnchorA.Set(randvertex.x, randvertex.y)
            self.joint_def.localAnchorB.Set(0, 0)
            self.joint_def.maxMotorTorque = self.torque[i]
            self.joint_def.motorSpeed = -Car.motorSpeed
            if i == self.motor_wheel_index:
                self.joint_def.enableMotor = True
            else:
                self.joint_def.enableMotor = False
            self.joint_def.collideConnected = False
            self.joint_def.bodyA = self.chassis.body
            self.joint_def.bodyB = self.wheels[i].body
            world.CreateJoint(self.joint_def)

        # Initial state in game
        self.health = Car.max_health
        self.isDead = False
        self.linear_vel = 0
        self.xy_pos = (0, 0)
        self.max_dist = 0

    @staticmethod
    def create_random_car(world: b2World, seed: int, seed_index: int):
        """
        Creates a random Car object.
        :param world: b2World where the Car will be used
        :param seed: seed for the random car
        :param seed_index: allow different car at the start
        :return: the newly created Car object
        """

        # List sizes
        number_of_wheels = 2
        number_of_chassis_vertices = 4

        wheel_radius_values = []
        wheel_vertex_values = []
        chassis_vertex_values = []
        
        random.seed(seed*seed_index)
        motor_wheel_index = random.randint(0, 1)

        for i in range(number_of_wheels):
            wheel_radius_values.append(random.random() * Wheel.maxRadius + Wheel.minRadius)

        chassis_vertex_values.append(b2Vec2(random.random() * Chassis.maxAxis + Chassis.minAxis, 0))
        chassis_vertex_values.append(b2Vec2(0, random.random() * Chassis.maxAxis + Chassis.minAxis))
        chassis_vertex_values.append(b2Vec2(-random.random() * Chassis.maxAxis - Chassis.minAxis, 0))
        chassis_vertex_values.append(b2Vec2(0, -random.random() * Chassis.maxAxis - Chassis.minAxis))

        index_left = list(range(number_of_chassis_vertices))
        for i in range(number_of_wheels):
            next_index = int(random.random() * (len(index_left) - 1))
            wheel_vertex_values.append(index_left[next_index])
            # remove the last used index from index_left
            index_left = index_left[:next_index] + index_left[next_index + 1:]

        return Car(world, wheel_radius_values, wheel_vertex_values, motor_wheel_index, chassis_vertex_values)

    def kill(self) -> None:
        """
        Kills this Car.
        """
        self.health = 0
        self.isDead = True

    def dcr_health(self) -> None:
        """
        Decreases this Car's health by 2.
        """
        self.health -= 2

    def set_pos_and_vel(self, pos: b2Vec2, vel: b2Vec2) -> None:
        """
        Sets the position and linear velocity of this Car.
        :param pos: new position
        :param vel: new velocity
        """
        if not self.isDead:
            self.xy_pos = pos
            self.linear_vel = vel
            self.update_health()
            self.update_max_dist()

    def update_health(self) -> None:
        """
        Updates the health of this Car.
        """
        if self.linear_vel < 0.0001:
            self.dcr_health()
            if self.health <= 0:
                self.kill()

    def update_max_dist(self) -> None:
        """
        Updates the maximum distance reached by this Car.
        """
        self.max_dist = self.xy_pos[0] - Car.start_position.x

    def print_info(self) -> None:
        """
        Prints information about this Car.
        """
        if not self.isDead:
            self.log.info("Velocity:", self.linear_vel, " Position:", self.xy_pos, " Health:", self.health)
        else:
            self.log.info("Dead")

    @staticmethod
    def get_top_cars(car_list: list, n: int) -> list:
        """
        gives the top n cars in the list, based on their distance
        :param car_list: list of cars
        :param n: number of best cars
        :return: list of car having the best distance, reversed ordered by their traveled distance (list[0] == best car)
        """
        return sorted(car_list, key=lambda car: car.max_dist, reverse=True)[:n]
