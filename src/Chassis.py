# Object physics
from Box2D import b2World, b2BodyDef, b2FixtureDef, b2PolygonShape, b2_dynamicBody, b2Vec2
# Type alias
from typing import List


class Chassis:
    """
    A class that represent a Car's chassis.
    """

    # Default chassis attributes
    maxAxis = 1.1
    minAxis = 0.1
    minDensity = 50
    maxDensity = 100
    density = 5
    number_of_vertices = 4

    def __init__(self, world: b2World, vertex_list: List[b2Vec2], position: b2Vec2):
        """
        Initializes an object of class Chassis.
        :param world: b2World where the chassis will be used
        :param vertex_list: list of the 4 vertices of the chassis
        :param position: initial position of the chassis
        """
        assert len(vertex_list) == Chassis.number_of_vertices, "The car's chassis must have exactly 4 vertices."
        self.vertex_list = vertex_list

        body_def = b2BodyDef()
        body_def.type = b2_dynamicBody
        body_def.position.Set(position.x, position.y)
        self.body = world.CreateBody(body_def)

        # Create part by part
        num_parts = len(vertex_list)
        self.parts = []
        for i in range(num_parts):
            self.create_chassis_part(vertex_list[i], vertex_list[(i+1) % num_parts])
        self.body.vertex_list = vertex_list

    def create_chassis_part(self, vertex1: b2Vec2, vertex2: b2Vec2) -> None:
        """
        Creates one edge of the chassis, between the two given vertices.
        :param vertex1: starting position of the edge
        :param vertex2: ending position of the edge
        """
        vertex_list = [vertex1, vertex2, b2Vec2(0, 0)]
        fix_def = b2FixtureDef()
        fix_def.shape = b2PolygonShape()
        fix_def.density = Chassis.density
        fix_def.friction = 10
        fix_def.restitution = 0.0
        fix_def.filter.groupIndex = -1
        fix_def.shape = b2PolygonShape(vertices=vertex_list)
        self.body.CreateFixture(fix_def)
