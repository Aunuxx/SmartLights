from SmartLights.traffic.constants import CardinalRoadShapes, RoadWays, Direction
from SmartLights.traffic import Light



class Lane:
    def __init__(self, turning: int, side: int) -> None:
        """
        Turning is a cardinal direction
        """
        self.turning = turning
        self.side = side


class Road:
    def __init__(self, shape: int, sides: tuple[int, int]):
        """
        See constants for shape enum.  
        Sides tuple containing a tuple list of Lane,  
        tuple[0] and tuple[tuple[0]] refers to the lowest cardinal direction.  
            N: 0 | E: 1 | S: 2 | W: 3.
        """
        self.shape = shape
        self.sides = sides




class Endpoint:
    """
    Ends of roads to be used as points of action by carSpawner and carDespawner
    """
    pos: tuple[int, int] = (0, 0)
    spawnDirection: Direction
    def __init__(self, pos: tuple[int, int], spawnDirection: Direction):
        self.pos = pos
        self.spawnDirection = spawnDirection


class Intersection:
    def __init__(self, dir: int, lanes: list[Lane]):
        self.dir = dir
        self.lanes = lanes

