from enum import Enum


class CardinalDirections(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

class CardinalRoadShapes(Enum):
    NE = 0
    NS = 1
    NW = 2
    SE = 3
    SW = 4
    WE = 5

class RoadWays(Enum):
    W1A = "oneWayAway"
    W1B = "oneWayToward"
    W2 = "twoWay"

class LightColors(Enum):
    OFF = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    STOP = 4
    YEILD = 5


class Direction(Enum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270