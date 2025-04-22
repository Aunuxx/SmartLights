from SmartLights.traffic.road import Road, Intersection, Lane
from SmartLights.simulation import Position
from SmartLights.simulation.draw import DrawObject

road = Road((0,0), [[Lane((1, 1, 0), 0, 1)], [Lane((0, 1, 0), 0, 0)]], 15)
# Road now accepets list[list[Road]] not list[Road],
# list[list[Road]] oppeates as a list[tuple[Road, Road]]
# since python does not allow direct assignment to tuple


assert isinstance(road.pos, Position)


intersection = Intersection([]) # Intersection now dirives pos from sim array indexes on draw_update

assert isinstance(intersection.pos, Position)


lanes: list[Lane] = []
lanes.append(Lane((1, 1, 0), 0, 1))
lanes.append(Lane((0, 1, 0), 0, 0))
lanes.append(Lane((1, 0, 1), 1, 1))
lanes.append(Lane((0, 1, 0), 1, 0))
lanes.append(Lane((0, 1, 1), 2, 1))
lanes.append(Lane((0, 1, 0), 2, 0))


for lane in lanes:
    if not lane.isEntering:
        assert lane.turning == (0, 1, 0)
    intersection.add_child(lane)
    assert lane.parent is intersection
    assert isinstance(lane, DrawObject)

assert isinstance(road, DrawObject)
assert isinstance(intersection, DrawObject)
assert isinstance(intersection.children, list)

print("Passed all tests")
