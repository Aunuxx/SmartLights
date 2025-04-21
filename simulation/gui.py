import time
import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
from SmartLights.traffic.constants import *
from SmartLights.traffic.road import Lane, Road, Intersection
from SmartLights.traffic import Light
from SmartLights.simulation.simulation import Simulation
from SmartLights.simulation import Position
from SmartLights.simulation.draw import DrawObject, Drawable, dpgDrawObject

WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000


center = (SIZE/2,SIZE/2)
triangles = [
    (center, (0,0), (SIZE/2,0)),
    (center, (SIZE/2,0), (SIZE,0)),
    (center, (SIZE,0), (SIZE, SIZE/2)),
    (center, (SIZE, SIZE/2), (SIZE, SIZE)),
    (center, (SIZE, SIZE), (SIZE/2, SIZE)),
    (center, (SIZE/2, SIZE), (0, SIZE)),
    (center, (0, SIZE), (0, SIZE/2)),
    (center, (0, SIZE/2), (0,0))
]

drawqueue: list[Drawable] = []

sim = Simulation()


sim.set_cell((0,0), Intersection([
    Lane((0, 1, 0), 0, 0),
    Lane((0, 1, 0), 1, 0),
    Lane((0, 1, 0), 1, 0),
    Lane((0, 1, 0), 2, 0),

    Lane((1, 1, 0), 0, 1),
    Lane((1, 0, 1), 1, 1),
    Lane((1, 0, 1), 1, 1),
    Lane((0, 1, 0), 2, 1)
    ]))
sim.set_cell((1,0), Intersection([
    Lane((0, 1, 0), 0, 0),
    Lane((0, 1, 0), 1, 0),
    Lane((0, 1, 0), 1, 0),
    Lane((0, 1, 0), 2, 0),
    Lane((0, 1, 0), 3, 0),
    Lane((0, 1, 0), 3, 0),

    Lane((0, 1, 0), 0, 1),
    Lane((0, 1, 0), 1, 1),
    Lane((0, 1, 0), 1, 1),
    Lane((0, 1, 0), 2, 1),
    Lane((1, 0, 1), 3, 1),
    Lane((1, 0, 1), 3, 1),
    ]))

def context_menu_callback(sender: int, app_data: int, user_data: int) -> None:
    print(f"Menu item '{user_data}' clicked")



def get_item_cell(user_data: int | str = "context_popup") -> tuple[int, int]:
    pos = dpg.get_item_pos(user_data)
    pos[1] = pos[1] - dpg.get_item_height(user_data)
    cell = int(pos[0]/SIZE), int(pos[1]/SIZE)
    return cell


def draw_update(app_data: int) -> None:
    dpg.draw_rectangle((0,0), (WINDOWWIDTH, WINDOWHEIGHT-100), color=(70, 70, 70), fill=(70, 70, 70), parent=app_data)
    sim.draw(app_data)
    for d in drawqueue:
        d.draw(app_data)



def delete_cell(sender: int, app_data: int, user_data: int) -> None:
    cell = get_item_cell()
    sim.rm_cell(cell)
    draw_update(draw_list)


def intersection_popup() -> None:
    cur = get_item_cell()
    sim[cur[0]][cur[1]].pos = Position(0, 0)
    sim[cur[0]][cur[1]].draw("Intersection")
    for tri in triangles:
        dpg.draw_triangle(*tri, parent="Intersection", color=(255,255,0,100))
    dpg.configure_item("Intersection", show=True, pos=dpg.get_item_pos("context_popup"))


def click_handler(sender: int, app_data: int, user_data: int) -> None:
    pos = dpg.get_mouse_pos()
    cur = get_item_cell()
    if dpg.is_item_hovered("Intersection"):
        for t in range(len(triangles)):
            if point_in_triangle(pos, *triangles[t]):
                if user_data == 0:
                    print(cur)
                    sim[cur[0]][cur[1]].add_child(Lane((0, 1, 0), int(t/2), (t+1)%2))
                    sim[cur[0]][cur[1]].draw("Intersection")
                    for tri in triangles:
                        dpg.draw_triangle(*tri, parent="Intersection", color=(255,255,0,100))
                elif user_data == 1:
                    for l in range(len(sim[cur[0]][cur[1]].children)):
                        c = sim[cur[0]][cur[1]].children[l]
                        if isinstance(c, Lane) and c.side == int(t/2) and c.isEntering == (t+1)%2:
                            del sim[cur[0]][cur[1]].children[l]
                            sim[cur[0]][cur[1]].draw("Intersection")
                            for tri in triangles:
                                dpg.draw_triangle(*tri, parent="Intersection", color=(255,255,0,100))
                            break
                draw_update(draw_list)


def point_in_triangle(pt: tuple[float, float], a: tuple[float, float],
                    b: tuple[float, float], c: tuple[float, float]) -> bool:
    # Barycentric technique
    def sign(p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]) -> float:
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - \
               (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    d1 = sign(pt, a, b)
    d2 = sign(pt, b, c)
    d3 = sign(pt, c, a)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)


def create_intersection() -> None:
    cur = get_item_cell()
    intersection = Intersection([])
    sim[cur[0]][cur[1]] = intersection
    intersection_popup()


dpg.create_context()

with dpg.theme() as canvas_theme, dpg.theme_component():
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0,0)
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255,255,255,255))


with dpg.handler_registry():
    dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left, user_data=0, callback=click_handler)
    dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Right, user_data=1, callback=click_handler)


with dpg.window(label="Modify an Intersection", tag="Intersection", show=False, modal=True,
                no_title_bar=False, width=SIZE+20, height=SIZE+50):
    pass



with dpg.window(width=WINDOWWIDTH, height=100, label="Menu", no_move=True,
                no_scrollbar=True, no_collapse=True, no_close=True, no_title_bar=True):
    drawlist = dpg.add_drawlist(width=WINDOWWIDTH, height=WINDOWHEIGHT)
    dpg.draw_rectangle((0, 0), (70, 70), parent=drawlist, color=WHITE, fill=(100, 100, 100))


with dpg.window(width=WINDOWWIDTH, height=WINDOWHEIGHT-100, pos=(0, 100),
                label="Simulation", no_move=True, no_collapse=True, no_close=True, no_title_bar=True):
    global draw_list
    draw_list = dpg.add_drawlist(width=WINDOWWIDTH, height=WINDOWHEIGHT-100, pos=(0, 100))
    draw_update(draw_list)

    with dpg.popup(parent=draw_list, mousebutton=dpg.mvMouseButton_Left, tag="context_popup"):
        dpg.add_menu_item(label="New Intersection",     callback=create_intersection)
        dpg.add_menu_item(label="Modify Intersection",  callback=intersection_popup)
        dpg.add_menu_item(label="New Endpoint",         callback=context_menu_callback)
        dpg.add_menu_item(label="Modify Endpoint",      callback=context_menu_callback)
        dpg.add_menu_item(label="Delete cell",          callback=delete_cell)



dpg.create_viewport(width=1000, height=1000, title="test")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
