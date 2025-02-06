from SmartLights.traffic.Constants import RoadWays, LightColors, Direction
from threading import Thread, Event
from collections.abc import Callable
import time


class Light:
    class LightTiming(Thread):
        def __init__(self, target: Callable[[],None] | None) -> None:
            self.flash = True
            if target is not None:
                super().__init__(target=target)
                self.start()
    
    def __init__(self) -> None:
        self.color = LightColors.OFF
        self.flashing: Light.LightTiming = Light.LightTiming(None)
    
    def setColor(self, color: LightColors) -> None:
        self.flashing.flash = False
        if color.value > LightColors.GREEN.value:
            self.flash(color)
            return
        self.color = color
    
    def green2Red(self, delay: int) -> None:
        def _call() -> None:
            self.color = LightColors.YELLOW
            time.sleep(delay)
            self.color = LightColors.RED
        self.LightTiming(_call)
    
    def red2Green(self, delay: int) -> None:
        def _call() -> None:
            time.sleep(delay)
            self.color = LightColors.GREEN
        self.LightTiming(_call)
    
    def flash(self, color: LightColors) -> None:
        def _call() -> None:
            time.sleep(0.1)
            while self.flashing.flash:
                self.color = color
                time.sleep(.5)
                self.color = LightColors.OFF
                time.sleep(.5)
        self.flashing = self.LightTiming(_call)






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
