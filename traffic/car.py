from SmartLights.traffic.constants import ROTATION
from SmartLights.traffic.road import Endpoint
from SmartLights.simulation import Position
from SmartLights.simulation.draw import DrawObject
from math import atan2, degrees
import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
import random

class Car(DrawObject):
    MAXSPEED: int = 200
    pos: Position
    vel: Position
    speed: int = 0
    facing: int = 0
    """Cardinal direction, see constants.py for more information."""
    waiting: int = 0
    stopped: bool = True
    def __init__(self, endpoint: Endpoint) -> None:
        self.pos = endpoint.pos + ROTATION[endpoint.dir]

    def angle(self, p1: tuple[int, int], p2: tuple[int, int]) -> float:
        """
        Calculate the angle between the line formed by two points and the line of 0º.
        """
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        angle = degrees(atan2(dx, dy))
        return float(angle % 360)

    def draw(self, app_data: int | str) -> int:
        dpg.draw_rectangle((*self.pos-(20,20),), (*self.pos+(20,20),), parent=app_data, color=(255,0,255))
        return 0

    # def tick(self) -> None:
    #     if self.stopped:
    #         self.waiting += 1
    #     self.facing = int(self.angle(self.pos, self.vel))


class CarManager:
    vehicles: list[Car] = []
    endpoints: list[Endpoint] = []

    def spawnCar(self) -> None:
        endpoint  = random.randint(0, len(self.endpoints))
        v = Car(self.endpoints[endpoint])
        
        self.vehicles.append(v)



