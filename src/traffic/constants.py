from enum import Enum


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
    WEST = 90
    SOUTH = 180
    EAST = 270