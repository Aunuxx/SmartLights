import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
from SmartLights.traffic.constants import *
from SmartLights.traffic.road import Lane, Road, Intersection
from SmartLights.traffic import Light
from SmartLights.simulation import Engine

WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000

engine = Engine()

intersection = Intersection((0, 0), [
    Lane((0, 1, 0), 0, 0),
    Lane((0, 1, 0), 1, 0),
    Lane((0, 1, 0), 1, 0),
    Lane((0, 1, 0), 2, 0),

    Lane((1, 1, 0), 0, 1),
    Lane((1, 0, 1), 1, 1),
    Lane((1, 0, 1), 1, 1),
    Lane((0, 1, 0), 2, 1)
    ])
intersection2 = Intersection((SIZE, 0), [
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
    ])


def check_mouse_pos() -> None:
    # print(dpg.get_mouse_pos(), dpg.get_win)
    print(int(dpg.get_mouse_pos()[0]/SIZE), int(dpg.get_mouse_pos()[1]/SIZE))

def draw_context_menu(pos: tuple[float, float]) -> None:
    with dpg.window(width=200, height=200, label="Create a new...",
                    pos=pos, no_collapse=True, no_scrollbar=True, modal=True):
        drawlist = dpg.add_drawlist(width=WINDOWWIDTH, height=WINDOWHEIGHT)
        dpg.draw_rectangle((0, 0), (70, 70), parent=drawlist, color=WHITE, fill=(100, 100, 100))
        dpg.draw_rectangle((0, 0), (140, 140), parent=drawlist, color=WHITE, fill=(100, 100, 100))




dpg.create_context()


with dpg.theme() as canvas_theme, dpg.theme_component():
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0,0)
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255,255,255,255))


with dpg.window(width=WINDOWWIDTH, height=100, label="Menu", no_move=True, no_scrollbar=True, no_collapse=True):
    drawlist = dpg.add_drawlist(width=WINDOWWIDTH, height=WINDOWHEIGHT)
    dpg.draw_rectangle((0, 0), (70, 70), parent=drawlist, color=WHITE, fill=(100, 100, 100))

with dpg.window(width=WINDOWWIDTH, height=WINDOWHEIGHT-100, pos=(0, 100),
                label="Simulation", no_move=True, no_collapse=True):
    drawlist = dpg.add_drawlist(width=WINDOWWIDTH, height=WINDOWHEIGHT, pos=(0, 100))
    intersection.draw(drawlist)
    intersection2.draw(drawlist)
    draw_context_menu((200, 200))
    # draw_intersection(drawlist, 0, 0, intersection)
    # draw_intersection(drawlist, SIZE, 0, intersection)
    # draw_road(drawlist, 0, 0, road)
    engine.add(check_mouse_pos)
    engine.start()



dpg.create_viewport(width=1000, height=1000, title="test")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
