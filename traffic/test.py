from SmartLights.traffic.road import Road, Intersection, Lane
from SmartLights.simulation import Position
from SmartLights.simulation.draw import DrawObject

road = Road((0,0), [Lane((1, 1, 0), 0, 1), Lane((0, 1, 0), 0, 0)], 15)

assert isinstance(road.pos, Position)


intersection = Intersection((0, 150), [])

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
