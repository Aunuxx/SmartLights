from SmartLights.src.traffic.Constants import Direction
from SmartLights.traffic.Road import Endpoint
import random
from math import atan2, degrees

class Car:
    MAXSPEED:int = 200
    pos: tuple[int, int] = (0, 0)
    vel: tuple[int, int] = (0, 0)
    speed: int = 0
    facing: int = 0 # int for granulatiry
    waiting: int = 0
    stopped: bool = True
    def __init__(self, endpoint: Endpoint) -> None:
        self.pos = endpoint.pos
        self.facing = endpoint.spawnDirection.value

    def angle(self, p1: tuple[int, int], p2: tuple[int, int]) -> float:
        """
        Calculate the angle between the line formed by two points and the line of 0º.
        """
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        angle = degrees(atan2(dx, dy))
        return float(angle % 360)


    def tick(self) -> None:
        if self.stopped:
            self.waiting += 1
        self.facing = int(self.angle(self.pos, self.vel))


class CarManager:
    cars: list[Car] = []
    endpoints: list[Endpoint] = []

    def spawnCar(self) -> None:
        endpoint  = random.randint(0, len(self.endpoints))
        car = Car(self.endpoints[endpoint])
        
        self.cars.append(car)



