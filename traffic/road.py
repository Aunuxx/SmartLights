import dearpygui.dearpygui as dpg
from SmartLights.simulation.draw import draw_backplate, draw_dotted_line
from SmartLights.traffic.constants import *
from SmartLights.traffic import Light



class Lane:
    def __init__(self, turning: int, side: int) -> None:
        """
        Turning is a cardinal direction
        Side is the cardinal direction reletive to the center of the intersection
        """
        self.turning = turning
        self.side = side
    def draw(lane, app_data: int, x: int, y: int) -> None:
        dpg.draw_line((x+SIZE/2,y+SIZE/2), (x+ROTATIONX[lane.side], y+ROTATIONY[lane.side]), parent=app_data, thickness=LANESIZE, color=STREET)


class Road:
    def __init__(self, shape: int, sides: tuple[int, int], pos: tuple[int, int]):
        self.shape = shape
        self.sides = sides
        self.pos = pos
    def draw_road(road, app_data: int, x: int, y: int) -> None:
        draw_backplate(app_data, x, y)
        lanes = road.sides[0] + road.sides[1]
        roadThickness = lanes * LANESIZE
        offset = ((road.sides[0] * -LANESIZE) + (road.sides[1] * LANESIZE))/2
        print(offset)

        dpg.draw_circle((x+SIZE/2+offset,y+SIZE/2), roadThickness/2, parent=app_data, color=STREET, fill=STREET)

        # Roads
        if road.shape in N: # N
            dpg.draw_line((x+SIZE/2+offset,y+SIZE/2), (x+ROTATIONX[0]+offset, y+ROTATIONY[0]), parent=app_data, thickness=roadThickness, color=STREET)
        if road.shape in E: # E
            dpg.draw_line((x+SIZE/2,y+SIZE/2+offset), (x+ROTATIONX[1], y+ROTATIONY[1]+offset), parent=app_data, thickness=roadThickness, color=STREET)
        if road.shape in S: # S
            dpg.draw_line((x+SIZE/2+offset,y+SIZE/2), (x+ROTATIONX[2]+offset, y+ROTATIONY[2]), parent=app_data, thickness=roadThickness, color=STREET)
        if road.shape in W: # W
            dpg.draw_line((x+SIZE/2,y+SIZE/2+offset), (x+ROTATIONX[3], y+ROTATIONY[3]+offset), parent=app_data, thickness=roadThickness, color=STREET)
        
        # Yellow Lines
        if road.sides[0] != 0 and road.sides[1] != 0:
            if road.shape in N: # N
                draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2), 0, YELLOW)
            if road.shape in E: # E
                draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2), 1, YELLOW)
            if road.shape in S: # S
                draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2), 2, YELLOW)
            if road.shape in W: # W
                draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2), 3, YELLOW)
        
        # White Lines
        if road.sides[0] > 1:
            for i in range(1,road.sides[0],1):
                if road.shape in N: # N
                    draw_dotted_line(app_data, (x+SIZE/2-(LANESIZE*i), y+SIZE/2), 0, WHITE)
                if road.shape in E: # E
                    draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2-(LANESIZE*i)), 1, WHITE)
                if road.shape in S: # S
                    draw_dotted_line(app_data, (x+SIZE/2-(LANESIZE*i), y+SIZE/2), 2, WHITE)
                if road.shape in W: # W
                    draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2-(LANESIZE*i)), 3, WHITE)
        if road.sides[1] > 1:
            for i in range(1,road.sides[1],1):
                if road.shape in N: # N
                    draw_dotted_line(app_data, (x+SIZE/2+(LANESIZE*i), y+SIZE/2), 0, WHITE)
                if road.shape in E: # E
                    draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2+(LANESIZE*i)), 1, WHITE)
                if road.shape in S: # S
                    draw_dotted_line(app_data, (x+SIZE/2+(LANESIZE*i), y+SIZE/2), 2, WHITE)
                if road.shape in W: # W
                    draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2+(LANESIZE*i)), 3, WHITE)
    def draw(self, app_data: int) -> None:
        self.draw_road(app_data, self.pos[0], self.pos[1])




class Endpoint:
    """
    Ends of roads to be used as points of action by carSpawner and carDespawner
    """
    pos: tuple[int, int] = (0, 0)
    spawnDirection: Direction
    def __init__(self, pos: tuple[int, int], spawnDirection: Direction):
        self.pos = pos
        self.spawnDirection = spawnDirection


class Intersection:
    def __init__(self, lanes: list[Lane], pos: tuple[int, int]):
        self.lanes = lanes
        self.pos = pos
    # def draw_lines(intersection, app_data: int, x: int, y: int) -> None:
    #     sides: list[int] = []
    #     for i in range(len(intersection.lanes)):
    #         if intersection.lanes[i].side not in sides:
    #             sides.append(intersection.lanes[i].side)
    #             draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2), intersection.lanes[i].side, YELLOW)
    def draw_intersection(intersection, app_data: int, x: int, y: int) -> None:
        draw_backplate(app_data, x, y)
        dpg.draw_circle((x+SIZE/2,y+SIZE/2), SIZE/6, parent=app_data, color=STREET, fill=STREET)
        for lane in intersection.lanes:
            lane.draw(app_data, x, y)
        # intersection.draw_lines(app_data, x, y)
    def draw(self, app_data: int) -> None:
        self.draw_intersection(app_data, self.pos[0], self.pos[1])




