from __future__ import annotations
from SmartLights.simulation import Engine, Position
from SmartLights.simulation.draw import DrawObject, Drawable
from SmartLights.traffic.constants import SIZE
from SmartLights.simulation.file_manager import FileManager
from typing import Iterator
import numpy as np
from SmartLights.traffic.road import Intersection

WIDTH = 4
HEIGHT = 4

fm = FileManager()

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

class Simulation(Drawable):
    def __init__(self) -> None:
        self.grid = np.empty((WIDTH, HEIGHT), dtype=DrawObject)
        self.engine = Engine()
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                self.grid[x][y] = DrawObject()

    def __getitem__(self, index: int): # type: ignore[no-untyped-def]
        return self.grid[index]
    
    def draw(self, app_data: int | str) -> int:
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[x][y].pos != (-1, -1):
                    self.grid[x][y].pos = Position(x*SIZE, y*SIZE)
                    self.grid[x][y].draw(app_data)
        return 0

    def set_cell(self, cell: tuple[int, int], data: DrawObject) -> None:
        self.grid[cell[0]][cell[1]] = data
        if isinstance(data, Intersection):
            data.pos = Position(*cell,)
            fm.write_intersection(data)

    def rm_cell(self, cell: tuple[int, int]) -> None:
        fm.rm_intersection(cell)
        self.grid[cell[0]][cell[1]] = DrawObject()






