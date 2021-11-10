# Object physics
from Box2D import b2World, b2Vec2, b2BodyDef, b2FixtureDef, b2CircleShape, b2_dynamicBody


class Wheel:
    """
    A class that represent a Wheel of a Car.
    """

    # Static variables
    maxRadius = 0.5  # Maximum wheel radius
    minRadius = 0.2  # Minimum wheel radius
    density = 2  # Mass density of a wheel (fixed)

    def __init__(self, world: b2World, radius: float, position: b2Vec2):
        """
        Initializes an object of class Wheel.
        :param world: b2World where the wheel will be used
        :param radius: radius of the wheel
        :param position: initial position of the wheel
        """
        body_def = b2BodyDef()
        body_def.type = b2_dynamicBody
        body_def.position.Set(position.x, position.y)
        fix_def = b2FixtureDef()
        fix_def.shape = b2CircleShape(radius=radius)
        fix_def.density = Wheel.density
        fix_def.friction = 1
        fix_def.restitution = 0.2
        fix_def.filter.groupIndex = -1

        self.body = world.CreateBody(body_def)
        self.body.CreateFixture(fix_def)
