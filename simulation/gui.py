import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
from SmartLights.traffic.constants import *
from SmartLights.traffic.road import *


SIZE = 150

GRASS = (19,109,21)
STREET = (50,50,50)
WHITE = (255,255,255)
YELLOW = (255,255,0)

rotationx: list[float] = [SIZE/2, SIZE, SIZE/2, 0]
rotationy: list[float] = [0, SIZE/2, SIZE, SIZE/2]
dottedRotationx: list[float] = [0, SIZE/13, 0, -SIZE/13]
dottedRotationy: list[float] = [-SIZE/13, 0, SIZE/13, 0]



intersection = Intersection(0, [Lane(0, 0), Lane(0, 2)])




def draw_dotted_line(app_data: int, p1: tuple[float, float], dir: int, color: tuple[int, ...]) -> None:
    for i in range(3):
        p1 = (p1[0] + dottedRotationx[dir], p1[1] + dottedRotationy[dir])
        prev = p1
        p1 = (p1[0] + dottedRotationx[dir], p1[1] + dottedRotationy[dir])
        dpg.draw_line(prev, p1, parent=app_data, thickness=3, color=color)

def draw_intersection_lines(app_data: int, x: int, y: int, intersection: Intersection) -> None:
    sides: list[int] = []
    for i in range(len(intersection.lanes)):
        if intersection.lanes[i].side not in sides:
            sides.append(intersection.lanes[i].side)
            draw_dotted_line(app_data, (x+SIZE/2, y+SIZE/2), intersection.lanes[i].side, YELLOW)

def draw_lane(app_data: int, x: int, y: int, dir: int, lane: Lane) -> None:
    dpg.draw_line((x+SIZE/2,y+SIZE/2), (x+rotationx[dir], y+rotationy[dir]), parent=app_data, thickness=20, color=STREET)
    # dpg.draw_line((x+SIZE/2,y+SIZE/2), (x+rotationx[dir], y+rotationy[dir]), parent=app_data, thickness=3, color=WHITE)

def draw_intersection(app_data: int, x: int, y: int, intersection: Intersection) -> None:
    dpg.draw_rectangle((x,y),(x+SIZE,y+SIZE), parent=app_data, color=GRASS, fill=GRASS)
    for i in range(0, len(intersection.lanes)):
        draw_lane(app_data, x, y, intersection.dir, intersection.lanes[i])
    dpg.draw_circle((x+SIZE/2,y+SIZE/2), SIZE/6, parent=app_data, color=STREET, fill=STREET)
    draw_intersection_lines(app_data, x, y, intersection)



dpg.create_context()


with dpg.theme() as canvas_theme, dpg.theme_component():
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0,0)
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255,255,255,255))


with dpg.window(width=500, height=500, label="Tutorial"):

    drawlist = dpg.add_drawlist(width=500, height=500)
    draw_intersection(drawlist, 0, 0, intersection)
    draw_intersection(drawlist, SIZE, 0, intersection)



dpg.create_viewport(width=800, height=800, title="test")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
