from __future__ import annotations
from typing import Optional
from collections.abc import Callable
import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
from SmartLights.traffic.constants import SIZE, DOTTEDROTATION, GRASS
from SmartLights.simulation import Pos, Position


class Drawable: # abstract class for dpgDrawObject and DrawObject to work in draw_list in gui
    """
    Abstract class
    """
    def __init__(self) -> None:
        pass
    def draw(self, app_data: int | str) -> int:
        return 0

class dpgDrawObject(Drawable): # Holds a dpg command for draw_list in gui
    def __init__(self, func: Callable[[], None]) -> None:
        self.func = func
    def draw(self, app_data: int | str) -> int:
        self.func()
        return 0

class DrawObject(Drawable): # Abstract class for Intersection, Road, Lane, etc
    """
    Abstract class
    """
    def __init__(self, pos: Pos = (-1, -1),
                parent: Optional[DrawObject] = None,
                children: Optional[list[DrawObject]] = None) -> None:
        self.pos: Position = Position(pos[0], pos[1])
        self.parent = parent
        self.children = children if children is not None else []
    def draw(self, app_data: int | str) -> int:
        for child in self.children:
            child.draw(app_data)
        return 0
    def add_child(self, child: DrawObject) -> None:
        child.parent = self
        self.children.append(child)
    def _draw_backplate(self, app_data: int | str) -> int: # Returns an int for parent var in dpg.draw_...
        o = dpg.draw_rectangle((*self.pos,), (*self.pos+(SIZE,SIZE),), parent=app_data, color=GRASS, fill=GRASS)
        if isinstance(o, int):
            return o
        return 0

def draw_dotted_line(app_data: int | str, p1: Position, dir: int, color: tuple[int, ...]) -> None:
    dpg.draw_circle((*p1,), 2, parent=app_data, color=color, fill=color)
    for i in range(3):
        p1 = p1 + DOTTEDROTATION[dir]
        prev = p1
        p1 = p1 + DOTTEDROTATION[dir]
        dpg.draw_line((*prev,), (*p1,), parent=app_data, thickness=3.5, color=color)

