import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
from SmartLights.traffic.constants import *
from SmartLights.traffic.road import Lane, Road, Intersection
from SmartLights.traffic import Light



intersection = Intersection((0, 0), [
    Lane((1, 1, 0), 0, 1),
    Lane((0, 1, 0), 0, 0),
    Lane((0, 1, 0), 1, 0),
    Lane((1, 0, 1), 1, 1),
    Lane((0, 1, 1), 2, 1),
    Lane((0, 1, 0), 2, 0)]
    )
road = Road((SIZE, 0), (1,1), 3)
# light = Light


dpg.create_context()


with dpg.theme() as canvas_theme, dpg.theme_component():
    dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0,0)
    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255,255,255,255))


with dpg.window(width=500, height=500, label="Tutorial"):

    drawlist = dpg.add_drawlist(width=500, height=500)
    intersection.draw(drawlist)
    # draw_intersection(drawlist, 0, 0, intersection)
    # draw_intersection(drawlist, SIZE, 0, intersection)
    # draw_road(drawlist, 0, 0, road)
    road.draw(drawlist)



dpg.create_viewport(width=800, height=800, title="test")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
