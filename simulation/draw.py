from __future__ import annotations
from typing import Optional
import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
from SmartLights.traffic.constants import SIZE, DOTTEDROTATION, GRASS
from SmartLights.simulation import Pos, Position

class DrawObject:
    def __init__(self, pos: Pos,
                parent: Optional[DrawObject] = None,
                children: Optional[list[DrawObject]] = None) -> None:
        if isinstance(pos, tuple):
            pos = Position(*pos)
        self.pos: Position = pos
        self.parent = parent
        self.children = children if children is not None else []
    def draw(self, app_data: int) -> None:
        for child in self.children:
            child.draw(app_data)
    def add_child(self, child: DrawObject) -> None:
        child.parent = self
        self.children.append(child)
    def draw_backplate(self, app_data: int) -> None:
        dpg.draw_rectangle((*self.pos,), (*self.pos+(SIZE,SIZE),), parent=app_data, color=GRASS, fill=GRASS)
        # print(self.pos, self.pos[0], self.pos[1])

def draw_dotted_line(app_data: int, p1: Position, dir: int, color: tuple[int, ...]) -> None:
    dpg.draw_circle((*p1,), 2, parent=app_data, color=color, fill=color)
    for i in range(3):
        p1 = p1 + DOTTEDROTATION[dir]
        prev = p1
        p1 = p1 + DOTTEDROTATION[dir]
        dpg.draw_line((*prev,), (*p1,), parent=app_data, thickness=3, color=color)

