from __future__ import annotations
from math import pow
import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
from SmartLights.simulation.draw import DrawObject, draw_dotted_line
from SmartLights.traffic.constants import SIZE, LANESIZE, STREET, GRASS, YELLOW, WHITE, ROTATION, DOTTEDROTATION, N, E, S, W, CardinalRoadShape
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
    
    def draw(lane, app_data: int) -> None:
        assert isinstance(lane.parent, DrawObject)
        # dpg.draw_line((*lane.parent.pos + SIZE/2,), (*lane.parent.pos + ROTATION[lane.side],), parent=app_data, thickness=LANESIZE, color=STREET)
        # dpg.draw_circle((*lane.parent.pos+SIZE/2-(LANESIZE, 0),), 2, parent=app_data, color=WHITE)

    def __repr__(self) -> str:
        return f"Lane"


class Road(DrawObject):
    def __init__(self, pos: Pos, lanes: list[list[Lane]], shape: int):
        super().__init__(pos)
        self.shape = shape
        self.lanes: list[list[Lane]] = lanes # Used closer to a tuple[list[Lane], list[Lane]] but is not for assignment purposes
        self.cover: tuple[Position, Position] # Cover to help intersection draws
        self.largest: float = 0.0 # Works with cover

    def draw_road(road, app_data: int) -> None:
        if len(road.lanes[0]) + len(road.lanes[1]) == 0:
            return
        roadThickness = (len(road.lanes[0]) + len(road.lanes[1])) * LANESIZE
        offset = ((len(road.lanes[0]) * LANESIZE) + (len(road.lanes[1]) * -LANESIZE))/2

        # Roads
        if road.shape in N: # N
            dpg.draw_line((*road.pos+SIZE/2+(offset,0),), (*road.pos+ROTATION[0]+(offset, 0),), parent=app_data, thickness=roadThickness, color=STREET)
        if road.shape in E: # E
            dpg.draw_line((*road.pos+SIZE/2+(0,offset),), (*road.pos+ROTATION[1]+(0, offset),), parent=app_data, thickness=roadThickness, color=STREET)
        if road.shape in S: # S
            dpg.draw_line((*road.pos+SIZE/2+(-offset,0),), (*road.pos+ROTATION[2]+(-offset, 0),), parent=app_data, thickness=roadThickness, color=STREET)
        if road.shape in W: # W
            dpg.draw_line((*road.pos+SIZE/2+(0,-offset),), (*road.pos+ROTATION[3]+(0, -offset),), parent=app_data, thickness=roadThickness, color=STREET)

    def draw_lines(road, app_data: int) -> None:
        # Yellow Lines
        if len(road.lanes[0]) != 0 and len(road.lanes[1]) != 0:
            if road.shape in N: # N
                draw_dotted_line(app_data, road.pos+SIZE/2, 0, YELLOW)
            if road.shape in E: # E
                draw_dotted_line(app_data, road.pos+SIZE/2, 1, YELLOW)
            if road.shape in S: # S
                draw_dotted_line(app_data, road.pos+SIZE/2, 2, YELLOW)
            if road.shape in W: # W
                draw_dotted_line(app_data, road.pos+SIZE/2, 3, YELLOW)
        
        # White Lines
        if len(road.lanes[0]) > 1:
            for i in range(1,len(road.lanes[0]),1):
                if road.shape in N: # N
                    draw_dotted_line(app_data, road.pos+SIZE/2+(LANESIZE*i, 0), 0, WHITE)
                    dpg.draw_circle((*road.pos+SIZE/2+(LANESIZE*i, 0),), 5, parent=app_data, color=WHITE, fill=WHITE)
                if road.shape in E: # E
                    draw_dotted_line(app_data, road.pos+SIZE/2+(0, LANESIZE*i), 1, WHITE)
                    dpg.draw_circle((*road.pos+SIZE/2+(0, LANESIZE*i),), 5, parent=app_data, color=WHITE, fill=WHITE)
                if road.shape in S: # S
                    draw_dotted_line(app_data, road.pos+SIZE/2+(-LANESIZE*i, 0), 2, WHITE)
                    dpg.draw_circle((*road.pos+SIZE/2+(-LANESIZE*i, 0),), 5, parent=app_data, color=WHITE, fill=WHITE)
                if road.shape in W: # W
                    draw_dotted_line(app_data, road.pos+SIZE/2+(0, -LANESIZE*i), 3, WHITE)
                    dpg.draw_circle((*road.pos+SIZE/2+(0, -LANESIZE*i),), 5, parent=app_data, color=WHITE, fill=WHITE)
        if len(road.lanes[1]) > 1:
            for i in range(1,len(road.lanes[1]),1):
                if road.shape in N: # N
                    draw_dotted_line(app_data, road.pos+SIZE/2-(LANESIZE*i, 0), 0, WHITE)
                    dpg.draw_circle((*road.pos+SIZE/2-(LANESIZE*i, 0),), 5, parent=app_data, color=WHITE, fill=WHITE)
                if road.shape in E: # E
                    draw_dotted_line(app_data, road.pos+SIZE/2-(0, LANESIZE*i), 1, WHITE)
                    dpg.draw_circle((*road.pos+SIZE/2+(LANESIZE*i, 0),), 5, parent=app_data, color=WHITE, fill=WHITE)
                if road.shape in S: # S
                    draw_dotted_line(app_data, road.pos+SIZE/2-(-LANESIZE * i, 0), 2, WHITE)
                    dpg.draw_circle((*road.pos+SIZE/2-(-LANESIZE * i, 0),), 5, parent=app_data, color=WHITE, fill=WHITE)
                if road.shape in W: # W
                    draw_dotted_line(app_data, road.pos+SIZE/2-(0, -LANESIZE * i), 3, WHITE)
                    dpg.draw_circle((*road.pos+SIZE/2-(0, -LANESIZE * i),), 5, parent=app_data, color=WHITE, fill=WHITE)


    def draw(self, app_data: int) -> None:
        self.draw_backplate(app_data)
        self.draw_road(app_data)
        self.draw_lines(app_data)
        super().draw(app_data)




class Endpoint:
    """
    Ends of roads to be used as points of action by carSpawner and carDespawner
    """
    def __init__(self, pos: Position, spawnDirection: int):
        self.pos = pos
        self.spawnDirection = spawnDirection


class Intersection(DrawObject):
    def __init__(self, pos: Pos, lanes: list[Lane]):
        super().__init__(pos)
        for lane in lanes:
            self.add_child(lane)

    def draw_intersection(self, app_data: int) -> None:
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

        print(lanes)

        p1 = (self.pos[0] + SIZE/2 + p1[0] * LANESIZE, self.pos[1] + SIZE/2 + p1[1] * LANESIZE)
        p2 = (self.pos[0] + SIZE/2 + p2[0] * LANESIZE, self.pos[1] + SIZE/2 + p2[1] * LANESIZE)

        dpg.draw_circle(p1, 5, parent=app_data, color=WHITE)
        dpg.draw_circle(p2, 5, parent=app_data, color=WHITE)

        # dpg.draw_rectangle(p1, p2, parent=app_data, color=STREET, fill=STREET)



    def draw(self, app_data: int) -> None:
        self.draw_backplate(app_data)
        self.draw_intersection(app_data)
        super().draw(app_data)




