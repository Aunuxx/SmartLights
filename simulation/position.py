from __future__ import annotations
from typing import Iterator

class Position:
    def __init__(self, x: float, y: float):
        self.pos: tuple[float, float] = (x, y)

    def __getitem__(self, index: int) -> float:
        return self.pos[index]

    def __iter__(self) -> Iterator[float]:
        return iter(self.pos)

    def __repr__(self) -> str:
        return f"({self.pos[0]}, {self.pos[1]})"

    def __mul__(self, a: Position | float) -> Position:
        if isinstance(a, Position):
            return Position(self.pos[0] * a[0], self.pos[1] * a[1])
        if isinstance(a, float):
            return Position(self.pos[0] * a, self.pos[1] * a)

    def __add__(self, a: tuple[float, float] | float) -> Position:
        if isinstance(a, tuple):
            return Position(self.pos[0] + a[0], self.pos[1] + a[1])
        if isinstance(a, float):
            return Position(self.pos[0] + a, self.pos[1] + a)

    def __sub__(self, a: tuple[float, float] | float) -> Position:
        if isinstance(a, tuple):
            return Position(self.pos[0] - a[0], self.pos[1] - a[1])
        if isinstance(a, float):
            return Position(self.pos[0] - a, self.pos[1] - a)


Pos = Position | tuple[float, float]