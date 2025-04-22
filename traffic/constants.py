from enum import Enum

SIZE = 250
LANESIZE = SIZE/10

CENTER = (SIZE/2,SIZE/2)

GRASS = (19,109,21)
STREET = (50,50,50)
WHITE = (255,255,255)
WHITEFADED = (255,255,255,128)
YELLOW = (255,255,0)

ROTATION: list[tuple[float, float]] = [
    (SIZE/2, 0),
    (SIZE, SIZE/2),
    (SIZE/2, SIZE),
    (0, SIZE/2)
    ]

DOTTEDROTATION: list[tuple[float,float]] = [
    (0, -SIZE/13), 
    (SIZE/13, 0), 
    (0, SIZE/13), 
    (-SIZE/13, 0)
    ]

ENDPOINTROTATION: list[tuple[tuple[float, float], tuple[float, float], tuple[float, float]]] = [
    ((SIZE/2, SIZE/5), (0, 0), (SIZE, 0)),
    ((SIZE-SIZE/5, SIZE/2), (SIZE, 0), (SIZE, SIZE)),
    ((SIZE/2, SIZE-SIZE/5), (SIZE, SIZE), (0, SIZE)),
    ((SIZE/5, SIZE/2), (0, SIZE), (0, 0))
]

CardinalRoadShape: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

#WSEN
#0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111
#1    2    3    4    5    6    7    8    9    10   11   12   13   14   15
N = [1, 3, 5, 7, 9, 11, 13, 15]
E = [2, 3, 6, 7, 10, 11, 14, 15]
S = [4, 5, 6, 7, 12, 13, 14, 15]
W = [8, 9, 10, 11, 12, 13, 14, 15]

class CardinalRoadShapes(Enum):
    """
    Determine the shape of the road useing theses steps:  
    0 or 1 for cardinal direction, e.g. N+E+S = 0111 (WSEN)  
    convert to dec, e.g. 0111 = 7 (8421)  
    you can use 0b0111 in substitute for int
    """
    N = 1 #
    E = 2 #
    NE = 3
    S = 4 #
    NS = 5
    ES = 6
    NES = 7
    W = 8 #
    NW = 9
    EW = 10
    NEW = 11
    SW = 12
    NSW = 13
    ESW = 14
    NESW = 15




class CardinalDirections(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


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