from SmartLights.traffic.constants import LightColors, Direction
from threading import Thread
from collections.abc import Callable
import time


class Light:
    class LightTiming(Thread):
        def __init__(self, target: Callable[[],None] | None) -> None:
            self.flash = True
            if target is not None:
                super().__init__(target=target)
                self.start()
    
    def __init__(self, id: int) -> None:
        self.id = id
        self.color = LightColors.OFF.value
        self.flashing: Light.LightTiming = Light.LightTiming(None)

        self.carsWaiting = 0
        self.faces = 0
        self.turns = 0
        self.carsApproaching = 0
        self.timeWaiting = 0
        self.priority = 0
        self.nextInstrction = 0
        self.instrctionWait = 0


    def __str__(self) -> str:
        return \
        f"color: {LightColors(self.color).name}\n"+\
        f"faces: {Direction(self.faces).name}\n"+\
        f"turns: {Direction(self.turns).name}\n"+\
        f"carsWaiting: {self.carsWaiting}\n"+\
        f"carsApproaching: {self.carsApproaching}\n"+\
        f"timeWaiting: {self.timeWaiting}\n"+\
        f"priority: {self.priority}\n"+\
        f"nextInstrction: {LightColors(self.nextInstrction).name}\n"+\
        f"instrctionWait: {self.instrctionWait}"


    def setColor(self, color: int) -> None:
        self.flashing.flash = False
        if color > LightColors.GREEN.value:
            self.flash(color)
            return
        self.color = color

    def green2Red(self, delay: int) -> None:
        def _call() -> None:
            self.color = LightColors.YELLOW.value
            time.sleep(delay)
            self.color = LightColors.RED.value
        self.LightTiming(_call)

    def red2Green(self, delay: int) -> None:
        def _call() -> None:
            time.sleep(delay)
            self.color = LightColors.GREEN.value
        self.LightTiming(_call)

    def flash(self, color: int) -> None:
        def _call() -> None:
            time.sleep(0.1)
            while self.flashing.flash:
                self.color = color
                time.sleep(.5)
                self.color = LightColors.OFF.value
                time.sleep(.5)
        self.flashing = self.LightTiming(_call)

