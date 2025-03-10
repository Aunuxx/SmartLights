from SmartLights.simulation import Engine
from SmartLights.traffic.road import Road, Lane
import numpy as np

WIDTH = 10
HEIGHT = 10

ROADSHAPE = dict(
    NE = 0,
    NS = 1,
    NW = 2,
    SE = 3,
    SW = 4,
    WE = 5
)

CARDINAL = dict(
    N = 0,
    E = 1,
    S = 2,
    W = 3
)


class Simulation:
    def __init__(self) -> None:
        self.engine = Engine()
        self.tiles = np.empty((WIDTH, HEIGHT), dtype=Road)

    def printArray(self) -> None:
        for w in range(WIDTH):
            for h in range(HEIGHT):
                print("[",end="")
                if (self.tiles[w][h] == None):
                    print("_", end="")
                else:
                    print(self.tiles[w][h], end="")
                    
                print("]",end="")
            print()

    def userInputValidation(self, set: list[str], message: str, invalidMessage: str) -> str:
        value = input(message)
        while value not in set:
            print(invalidMessage)
            value = input(message)
        return value

    def setLayoutC(self) -> None:
        for w in range(WIDTH):
            for h in range(HEIGHT):
                self.printArray()
                type = self.userInputValidation(["0", "1"],
                    "Enter tile type\n [0 = None, 1 = Road]:", "Wrong value for type, try again")

                if type == "1":
                    shape = ROADSHAPE[self.userInputValidation(["NE", "NS", "NW", "SE", "SW", "WE"],
                        "Road shape, write in all caps cardinal directions.\n" \
                        "Reletive to the center of the intersection a turn from" \
                        "south to north (stright) would be NS \n" \
                        "[NE, NS, NW, SE, SW, WE]",
                        "Not a valid shape")]
                    
                    nSides = self.userInputValidation(["1", "2"], "One way or two way [1, 2]",
                        "Not a valid amount of sides")
                    
                    sides: tuple[list[Lane], list[Lane|None]] = ([],[])
                    for nSide in range(int(nSides)):
                        nLanes = self.userInputValidation(["1","2","3","4","5","6","7","8","9","10"],
                            f"How many lanes in {nSide} direction", "Invlaid amount of lanes")
                        
                        for nLane in range(int(nLanes)):
                            print(f"For lane {nLane} in {nSide} direction.")

                            atIntersection = bool(self.userInputValidation(["True","False"],
                                "\tIs it at an intersection? [True, False]: ", "Invald value"))
                            turning = CARDINAL[self.userInputValidation(["N","E","S","W"],
                                "\tWhat direction does it turn? [N, E, S, W]: ", "Invlaid value")]
                            sides[nSide].append(Lane(int(turning), bool(atIntersection)))

                    self.tiles[w][h] = Road(int(shape), sides)




