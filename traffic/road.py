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
        dpg.draw_circle((*lane.parent.pos+SIZE/2-(LANESIZE, 0),), 2, parent=app_data, color=WHITE)


class Road(DrawObject):
    def __init__(self, pos: Pos, sides: tuple[int, int], shape: int):
        super().__init__(pos)
        self.shape = shape
        self.sides = sides
    
    def draw_road(road, app_data: int) -> None:
        lanes = road.sides[0] + road.sides[1]
        if lanes == 0:
            return
        roadThickness = lanes * LANESIZE
        offset = ((road.sides[0] * -LANESIZE) + (road.sides[1] * LANESIZE))/2

        dpg.draw_circle((*road.pos+SIZE/2+(offset, 0),), roadThickness/2, parent=app_data, color=STREET, fill=STREET)

        # Roads
        if road.shape in N: # N
            dpg.draw_line((*road.pos+SIZE/2+(offset,0),), (*road.pos+ROTATION[0]+(offset, 0),), parent=app_data, thickness=roadThickness, color=STREET)
        if road.shape in E: # E
            dpg.draw_line((*road.pos+SIZE/2+(0,offset),), (*road.pos+ROTATION[1]+(0, offset),), parent=app_data, thickness=roadThickness, color=STREET)
        if road.shape in S: # S
            dpg.draw_line((*road.pos+SIZE/2+(offset,0),), (*road.pos+ROTATION[2]+(offset, 0),), parent=app_data, thickness=roadThickness, color=STREET)
        if road.shape in W: # W
            dpg.draw_line((*road.pos+SIZE/2+(0,offset),), (*road.pos+ROTATION[3]+(0, offset),), parent=app_data, thickness=roadThickness, color=STREET)
    
    def draw_lines(road, app_data: int) -> None:
        # Yellow Lines
        if road.sides[0] != 0 and road.sides[1] != 0:
            if road.shape in N: # N
                draw_dotted_line(app_data, road.pos+SIZE/2, 0, YELLOW)
            if road.shape in E: # E
                draw_dotted_line(app_data, road.pos+SIZE/2, 1, YELLOW)
            if road.shape in S: # S
                draw_dotted_line(app_data, road.pos+SIZE/2, 2, YELLOW)
            if road.shape in W: # W
                draw_dotted_line(app_data, road.pos+SIZE/2, 3, YELLOW)
        
        # White Lines
        if road.sides[0] > 1:
            for i in range(1,road.sides[0],1):
                if road.shape in N: # N
                    draw_dotted_line(app_data, road.pos+SIZE/2-(LANESIZE*i, 0), 0, WHITE)
                if road.shape in E: # E
                    draw_dotted_line(app_data, road.pos+SIZE/2-(0, LANESIZE*i), 1, WHITE)
                if road.shape in S: # S
                    draw_dotted_line(app_data, road.pos+SIZE/2-(LANESIZE*i, 0), 2, WHITE)
                if road.shape in W: # W
                    draw_dotted_line(app_data, road.pos+SIZE/2-(0, LANESIZE*i), 3, WHITE)
        if road.sides[1] > 1:
            for i in range(1,road.sides[1],1):
                if road.shape in N: # N
                    draw_dotted_line(app_data, road.pos+SIZE/2+(LANESIZE*i, 0), 0, WHITE)
                if road.shape in E: # E
                    draw_dotted_line(app_data, road.pos+SIZE/2+(0, LANESIZE*i), 1, WHITE)
                if road.shape in S: # S
                    draw_dotted_line(app_data, road.pos+SIZE/2+(LANESIZE*i, 0), 2, WHITE)
                if road.shape in W: # W
                    draw_dotted_line(app_data, road.pos+SIZE/2+(0, LANESIZE*i), 3, WHITE)
    
    def draw(self, app_data: int) -> None:
        self.draw_backplate(app_data)
        self.draw_road(app_data)
        self.draw_lines(app_data)
        super().draw(app_data)




# class Endpoint:
#     """
#     Ends of roads to be used as points of action by carSpawner and carDespawner
#     """
#     pos: Pos
#     spawnDirection: Direction
#     def __init__(self, pos: Pos, spawnDirection: Direction):
#         self.pos = pos
#         self.spawnDirection = spawnDirection


class Intersection(DrawObject):
    def __init__(self, pos: Pos, lanes: list[Lane]):
        super().__init__(pos)
        for lane in lanes:
            self.add_child(lane)
    
    # def draw_lines(intersection, app_data: int, x: int, y: int) -> None:
    #     sides: list[int] = []
    #     for i in range(len(intersection.lanes)):
    #         if intersection.lanes[i].side not in sides:
    #             sides.append(intersection.lanes[i].side)
    #             draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2), intersection.lanes[i].side, YELLOW)
    
    def draw_intersection(self, app_data: int) -> None:
        # dpg.draw_circle((*self.pos+SIZE/2,), SIZE/6, parent=app_data, color=STREET, fill=STREET)

        lanes: list[tuple[int, int]] = [(0, 0), (0, 0), (0, 0), (0, 0)]
        for lane in self.children:
            if isinstance(lane, Lane):
                if lane.isEntering:
                    lanes[lane.side] = (lanes[lane.side][0], lanes[lane.side][1] + 1)
                else:
                    lanes[lane.side] = (lanes[lane.side][0] + 1, lanes[lane.side][1])
        roads: list[Road] = []
        for i in range(len(lanes)):
            road = Road(self.pos, (*lanes[i],), CardinalRoadShape[i])
            print(lanes[i])
            roads.append(road)
        for road in roads:
            road.draw_road(app_data)
        for road in roads:
            road.draw_lines(app_data)


    def draw(self, app_data: int) -> None:
        self.draw_backplate(app_data)
        self.draw_intersection(app_data)
        super().draw(app_data)




