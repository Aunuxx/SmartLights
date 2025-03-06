from SmartLights.traffic.constants import RoadWays, Direction



class Lane:
    def __init__(self) -> None:
        pass



class Side:
    def __init__(self) -> None:
        pass
    def __str__(self) -> str:
        return "test"



class Road:
    def __init__(self, ways:RoadWays, sides:list[Side]):
        """
        ways: oneway or twoway, use traffic.Constants.RoadWays
        sides[2]: list[0] should be the west side
        """
        self.ways = ways
        self.sides = sides
        assert len(sides) <= 2


class Endpoint:
    """
    Ends of roads to be used by carSpawner and carDespawner
    """
    pos: tuple[int, int] = (0, 0)
    spawnDirection: Direction
    def __init__(self, pos: tuple[int, int], spawnDirection: Direction):
        self.pos = pos
        self.spawnDirection = spawnDirection
