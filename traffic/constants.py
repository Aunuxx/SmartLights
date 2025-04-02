from enum import Enum

SIZE = 150
LANESIZE = SIZE/8

GRASS = (19,109,21)
STREET = (50,50,50)
WHITE = (255,255,255)
WHITEFADED = (255,255,255,128)
YELLOW = (255,255,0)

ROTATIONX: list[float] = [SIZE/2, SIZE, SIZE/2, 0]
ROTATIONY: list[float] = [0, SIZE/2, SIZE, SIZE/2]
DOTTEDROTATIONX: list[float] = [0, SIZE/13, 0, -SIZE/13]
DOTTEDROTATIONY: list[float] = [-SIZE/13, 0, SIZE/13, 0]

N = [0, 4, 5, 6]
S = [1, 4, 7, 9]
E = [2, 5, 7, 8]
W = [3, 6, 8, 9]

class CardinalDirections(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

class CardinalRoadShapes(Enum):
    N = 0
    E = 1
    S = 2
    W = 3
    NE = 4
    NS = 5
    NW = 6
    SE = 7
    SW = 8
    WE = 9


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