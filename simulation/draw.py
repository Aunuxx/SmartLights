from __future__ import annotations
from typing import Optional
import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
from SmartLights.traffic.constants import SIZE, DOTTEDROTATIONX, DOTTEDROTATIONY, GRASS
from SmartLights.simulation import Pos, Position

class DrawObject:
    def __init__(self, pos: Pos, zIndex: int,
                parent: Optional[DrawObject] = None,
                children: Optional[list[DrawObject]] = None) -> None:
        if isinstance(pos, tuple):  # Convert tuple to position if needed
            pos = Position(*pos)        
        self.pos: Position = pos
        self.parent = parent
        self.children = children if children is not None else []
    def draw(self, app_data: int) -> None:
        for child in self.children:
            child.draw(app_data)
    def addChild(self, child: DrawObject) -> None:
        child.parent = self
        self.children.append(child)
    def draw_backplate(self, app_data: int) -> None:
        dpg.draw_rectangle(self.pos, tuple(self.pos+(SIZE,SIZE)), parent=app_data, color=GRASS, fill=GRASS)

def draw_dotted_line(app_data: int, p1: Pos, dir: int, color: tuple[int, ...]) -> None:
    if isinstance(p1, tuple):  # Convert tuple to position if needed
        p1 = Position(*p1)
    dpg.draw_circle(p1, 2, parent=app_data, color=color, fill=color)
    for i in range(3):
        p1 = Position(p1[0] + DOTTEDROTATIONX[dir], p1[1] + DOTTEDROTATIONY[dir])
        prev = p1
        p1 = Position(p1[0] + DOTTEDROTATIONX[dir], p1[1] + DOTTEDROTATIONY[dir])
        dpg.draw_line(prev, p1, parent=app_data, thickness=3, color=color)

