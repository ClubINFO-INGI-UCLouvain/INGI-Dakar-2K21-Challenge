import random
import math
from Box2D import b2World, b2Vec2, b2BodyDef, b2Body, b2FixtureDef, b2PolygonShape
from typing import List


class Terrain:
    """
    Class that represents the terrain on which the game takes place.
    """

    # Default ground pieces values
    groundPieceWidth = 1.5
    groundPieceHeight = 0.15

    def __init__(self, world: b2World, seed: int):
        self.world = world
        self.seed = seed 

    def create_floor(self) -> List[b2Body]:
        """
        Creates the floor for the game.
        :return: a list containing all the ground pieces that represent the game floor
        """
        maxFloorTiles = 200
        last_tile = None
        tile_position = b2Vec2(-1, 0)
        floor_tiles = []
        random.seed(self.seed)
        for k in range(maxFloorTiles):
            last_tile = self.create_floor_tile(tile_position, (random.random() * 3 - 1.5) * 1.2 * k / maxFloorTiles)
            floor_tiles.append(last_tile)
            last_fixture = last_tile.fixtures
            # below is the fix for jagged edges: the vertex order was messed up, so sometimes the left bottom corner
            # would be connected to the top right corner of the previous tile
            if last_fixture[0].shape.vertices[3] == b2Vec2(0, 0):
                last_world_coords = last_tile.GetWorldPoint(last_fixture[0].shape.vertices[0])
            else:
                last_world_coords = last_tile.GetWorldPoint(last_fixture[0].shape.vertices[3])
            tile_position = last_world_coords
        return floor_tiles

    def create_floor_tile(self, position: b2Vec2, angle: float) -> b2Body:
        """
        Creates a floor tile.
        :param position: the position of the floor tile
        :param angle: the angle of the floor tile
        :return: the newly created floor tile
        """
        body_def = b2BodyDef()
        # body_def.position.Set(position.x, position.y)
        body_def.position = position
        body = self.world.CreateBody(body_def)
        fix_def = b2FixtureDef()
        fix_def.shape = b2PolygonShape()
        fix_def.friction = 0.5
        coords = []
        coords.append(b2Vec2(0, 0))
        coords.append(b2Vec2(0, Terrain.groundPieceHeight))
        coords.append(b2Vec2(Terrain.groundPieceWidth, Terrain.groundPieceHeight))
        coords.append(b2Vec2(Terrain.groundPieceWidth, 0))
        newcoords = self.rotate_floor_tile(coords, angle)
        fix_def.shape = b2PolygonShape(vertices=newcoords)  # setAsArray alt

        body.CreateFixture(fix_def)
        return body

    def rotate_floor_tile(self, coords: List[b2Vec2], angle: float) -> List[b2Vec2]:
        """
        Rototes q floor tile.
        :param coords: the coordinates of the floor tile to rotate
        :param angle: the angle to rotate with
        :return: the new coordinates of the floor tiles
        """
        newcoords = []
        for k in range(len(coords)):
            nc = b2Vec2(0, 0)
            nc.x = math.cos(angle) * (coords[k].x) - math.sin(angle) * (coords[k].y)
            nc.y = math.sin(angle) * (coords[k].x) + math.cos(angle) * (coords[k].y)
            newcoords.append(nc)
        return newcoords