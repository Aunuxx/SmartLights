import dearpygui.dearpygui as dpg # type: ignore[import-untyped]
from SmartLights.traffic.constants import SIZE, DOTTEDROTATIONX, DOTTEDROTATIONY, GRASS


def draw_backplate(app_data: int, x: int, y: int) -> None:
    dpg.draw_rectangle((x,y),(x+SIZE,y+SIZE), parent=app_data, color=GRASS, fill=GRASS)

def draw_dotted_line(app_data: int, p1: tuple[float, float], dir: int, color: tuple[int, ...]) -> None:
    dpg.draw_circle(p1, 2, parent=app_data, color=color, fill=color)
    for i in range(3):
        p1 = (p1[0] + DOTTEDROTATIONX[dir], p1[1] + DOTTEDROTATIONY[dir])
        prev = p1
        p1 = (p1[0] + DOTTEDROTATIONX[dir], p1[1] + DOTTEDROTATIONY[dir])
        dpg.draw_line(prev, p1, parent=app_data, thickness=3, color=color)

