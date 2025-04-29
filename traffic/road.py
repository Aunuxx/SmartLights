from __future__ import annotations
from math import pow
import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
from SmartLights.simulation.draw import DrawObject, draw_dotted_line
from SmartLights.traffic.constants import SIZE, LANESIZE, STREET, YELLOW, WHITE, ROTATION, N, E, S, W, ENDPOINTROTATION
from SmartLights.traffic import Light
from SmartLights.simulation import Pos, Position



class Lane(DrawObject):
    def __init__(self, turning: tuple[int, int, int], side: int, isEntering: int) -> None:
        """
        Turning is a cardinal direction
        Side is the cardinal direction reletive to the center of the intersection
        """
        self.turning = turning
        self.side = side
        self.isEntering = isEntering
        if not self.isEntering:
            assert self.turning == (0, 1, 0)
    
    def draw(lane, app_data: int | str) -> int:
        assert isinstance(lane.parent, Intersection)
        return 0

    def __repr__(self) -> str:
        return f"Lane"


class Road(DrawObject):
    """
    Implemented by Intersection.
    Defines Road draw locations relative to cell position.
    """
    def __init__(self, pos: Pos, lanes: list[list[Lane]], shape: int):
        super().__init__(pos)
        self.shape = shape
        self.lanes: list[list[Lane]] = lanes # Used closer to a tuple[list[Lane], list[Lane]] but is not for assignment purposes
        self.cover: tuple[Position, Position] # Cover to help intersection draws
        self.largest: float = 0.0 # Works with cover

    def draw_road(self, app_data: int | str) -> None:
        if len(self.lanes[0]) + len(self.lanes[1]) == 0:
            return
        roadThickness = (len(self.lanes[0]) + len(self.lanes[1])) * LANESIZE
        offset = ((len(self.lanes[0]) * LANESIZE) + (len(self.lanes[1]) * -LANESIZE))/2

        # Roads
        if self.shape in N: # N
            dpg.draw_line((*self.pos+SIZE/2+(offset,0),), (*self.pos+ROTATION[0]+(offset, 0),), parent=app_data, thickness=roadThickness, color=STREET)
        if self.shape in E: # E
            dpg.draw_line((*self.pos+SIZE/2+(0,offset),), (*self.pos+ROTATION[1]+(0, offset),), parent=app_data, thickness=roadThickness, color=STREET)
        if self.shape in S: # S
            dpg.draw_line((*self.pos+SIZE/2+(-offset,0),), (*self.pos+ROTATION[2]+(-offset, 0),), parent=app_data, thickness=roadThickness, color=STREET)
        if self.shape in W: # W
            dpg.draw_line((*self.pos+SIZE/2+(0,-offset),), (*self.pos+ROTATION[3]+(0, -offset),), parent=app_data, thickness=roadThickness, color=STREET)

    def draw_lines(self, app_data: int | str) -> None:
        # Yellow Lines
        if len(self.lanes[0]) != 0 and len(self.lanes[1]) != 0:
            if self.shape in N: # N
                draw_dotted_line(app_data, self.pos+SIZE/2, 0, YELLOW)
            if self.shape in E: # E
                draw_dotted_line(app_data, self.pos+SIZE/2, 1, YELLOW)
            if self.shape in S: # S
                draw_dotted_line(app_data, self.pos+SIZE/2, 2, YELLOW)
            if self.shape in W: # W
                draw_dotted_line(app_data, self.pos+SIZE/2, 3, YELLOW)
        
        # White Lines
        if len(self.lanes[0]) > 1:
            for i in range(1,len(self.lanes[0]),1):
                if self.shape in N: # N
                    draw_dotted_line(app_data, self.pos+SIZE/2+(LANESIZE*i, 0), 0, WHITE)
                if self.shape in E: # E
                    draw_dotted_line(app_data, self.pos+SIZE/2+(0, LANESIZE*i), 1, WHITE)
                if self.shape in S: # S
                    draw_dotted_line(app_data, self.pos+SIZE/2+(-LANESIZE*i, 0), 2, WHITE)
                if self.shape in W: # W
                    draw_dotted_line(app_data, self.pos+SIZE/2+(0, -LANESIZE*i), 3, WHITE)
        if len(self.lanes[1]) > 1:
            for i in range(1,len(self.lanes[1]),1):
                if self.shape in N: # N
                    draw_dotted_line(app_data, self.pos+SIZE/2-(LANESIZE*i, 0), 0, WHITE)
                if self.shape in E: # E
                    draw_dotted_line(app_data, self.pos+SIZE/2-(0, LANESIZE*i), 1, WHITE)
                if self.shape in S: # S
                    draw_dotted_line(app_data, self.pos+SIZE/2-(-LANESIZE * i, 0), 2, WHITE)
                if self.shape in W: # W
                    draw_dotted_line(app_data, self.pos+SIZE/2-(0, -LANESIZE * i), 3, WHITE)


    def draw(self, app_data: int | str) -> int:
        o = self._draw_backplate(app_data)
        self.draw_road(app_data)
        self.draw_lines(app_data)
        super().draw(app_data)
        return o


class Endpoint(DrawObject):
    """
    Ends of roads to be used as points of action by carSpawner and carDespawner
    """
    def __init__(self, pos: Position = Position(-1, -1), dir: int = 0):
        super().__init__(pos)
        self.dir = dir
    def draw(self, app_data: int | str) -> int:
        if self.parent:
            self.pos = self.parent.pos
            o = dpg.draw_triangle(
                (*self.pos+ENDPOINTROTATION[self.dir][0],),
                (*self.pos+ENDPOINTROTATION[self.dir][1],),
                (*self.pos+ENDPOINTROTATION[self.dir][2],),
                parent=app_data, color=(0, 0, 255, 100))
            if isinstance(o, int):
                return o
        return 0


class Intersection(DrawObject):
    """
    What is stored as a cell in simulation.grid.
    Implements Road and Endpoint.
    """
    def __init__(self, lanes: list[Lane]):
        super().__init__()
        self.endpoints: list[Endpoint] = [Endpoint(), Endpoint(), Endpoint(), Endpoint()]
        for lane in lanes:
            self.add_child(lane) # keep to make lane.parent = self

    def add_endpoint(self, endpoint: Endpoint) -> None:
        endpoint.parent = self
        self.endpoints[endpoint.dir] = endpoint

    def rm_endpoint(self, dir: int) -> None:
        self.endpoints[dir] = Endpoint()

    def _draw_intersection(self, app_data: int | str) -> None:
        lanes: list[list[list[Lane]]] = [[[],[]], [[],[]], [[],[]], [[],[]]]
        for lane in self.children:
            if isinstance(lane, Lane):
                lanes[lane.side][lane.isEntering].append(lane)
        roads: list[Road] = []
        for i in range(len(lanes)):
            road = Road(self.pos, lanes[i], int(pow(2, i)))
            roads.append(road)
        for road in roads:
            road.draw_road(app_data)
        for road in roads:
            road.draw_lines(app_data)


        p1: tuple[float, float] = (-len(lanes[0][1]), -len(lanes[1][1]))
        if len(lanes[0][1]) <= len(lanes[2][0]):
            p1 = (-len(lanes[2][0]), p1[1])
        if len(lanes[1][1]) <= len(lanes[3][0]):
            p1 = (p1[0], -len(lanes[3][0]))
        
        p2: tuple[float, float] = (len(lanes[0][0]), len(lanes[1][0]))
        if len(lanes[0][0]) <= len(lanes[2][1]):
            p2 = (len(lanes[2][1]), p2[1])
        if len(lanes[1][0]) <= len(lanes[3][1]):
            p2 = (p2[0], len(lanes[3][1]))

        p1 = (self.pos[0] + SIZE/2 + p1[0] * LANESIZE, self.pos[1] + SIZE/2 + p1[1] * LANESIZE)
        p2 = (self.pos[0] + SIZE/2 + p2[0] * LANESIZE, self.pos[1] + SIZE/2 + p2[1] * LANESIZE)

        dpg.draw_rectangle(p1, p2, parent=app_data, color=STREET, fill=STREET) # Cover rectangle
        
        # for side in range(4):
        #     for a in range(1, len(lanes[side][1]) + 1):
        #         offset = a * LANESIZE - LANESIZE / 2
        #         opposing = len(lanes[side][0]) * LANESIZE

        #         if side == 0:  # N
        #             x = p1[0] + offset
        #             y = p1[1] - LANESIZE / 2
        #         elif side == 1:  # E
        #             x = p2[0] + LANESIZE / 2
        #             y = p1[1] + offset
        #         elif side == 2:  # S
        #             x = p1[0] + offset
        #             y = p2[1] + LANESIZE / 2
        #         elif side == 3:  # W
        #             x = p1[0] - LANESIZE / 2
        #             y = p1[1] + offset

        #         dpg.draw_circle((x, y), radius=10, color=(255, 0, 0), fill=(255, 255, 0), parent=app_data)



    def draw(self, app_data: int | str) -> int:
        o = self._draw_backplate(app_data)
        self._draw_intersection(app_data)
        for e in self.endpoints:
            e.draw(app_data)
        super().draw(app_data)
        return o




