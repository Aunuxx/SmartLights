import json
from SmartLights.traffic import Light
from SmartLights.traffic.road import Intersection, Lane
from SmartLights.traffic.constants import SIZE

class FileManager:
    """
    Manages back end json file.
    """
    def __init__(self) -> None:
        self.outpath = "currentstate.json"

    def read_file(self) -> dict[str, list[dict[str, int]]]:
        with open(self.outpath, "r") as file:
            return dict(json.load(file))
        return {}

    def get_data(self, id: int, key: str) -> int:
        return self.read_file()["Lights"][id][key]

    def set_data(self, id: int, key: str, data: int) -> None:
        cs = self.read_file()["Lights"][id][key] = data
        with open(self.outpath, "w") as file:
            file.write(json.dumps(cs, indent=4))

    def get_light(self, id: int) -> Light:
        cs = self.read_file()["Lights"][id]
        out = Light(id)
        out.color = cs["color"]
        out.faces = cs["faces"]
        out.turns = cs["turns"]
        out.carsWaiting = cs["carsWaiting"]
        out.carsApproaching = cs["carsApproaching"]
        out.timeWaiting = cs["timeWaiting"]
        out.nextInstrction = cs["nextInstrction"]
        out.priority = cs["priority"]
        out.instrctionWait = cs["instrctionWait"]
        return out

    def write_light(self, light: Light) -> None:
        cs = self.read_file()

        cs["Lights"][light.id] = dict(
            color = light.color, # int
            faces = light.faces,
            turns = light.turns,
            carsWaiting = light.carsWaiting, # int
            carsApproaching = light.carsApproaching, # int
            timeWaiting = light.timeWaiting, # int
            priority = light.priority,
            nextInstrction = light.nextInstrction, # int
            instrctionWait = light.instrctionWait # int
        )

        with open(self.outpath, "w") as file:
            file.write(json.dumps(cs, indent=4))

    def rm_intersection(self, cell: tuple[int, int]) -> None:
        cs = self.read_file()
        cs["Intersections"][cell[0]][cell[1]] = dict() # type: ignore[index,assignment]
        with open(self.outpath, "w") as file:
            file.write(json.dumps(cs, indent=4))

    def write_intersection(self, intersection: Intersection) -> None:
        cs = self.read_file()

        nSide = 0
        eSide = 0
        sSide = 0
        wSide = 0

        for lane in intersection.children:
            if isinstance(lane, Lane):
                if lane.side == 0:
                    nSide += 1
                if lane.side == 1:
                    eSide += 1
                if lane.side == 2:
                    sSide += 1
                if lane.side == 3:
                    wSide += 1


        cs["Intersections"][int(intersection.pos[0]/SIZE)][int(intersection.pos[1]/SIZE)] = dict( # type: ignore[index,assignment]
            cellX = int(intersection.pos[0]/SIZE),
            cellY = int(intersection.pos[1]/SIZE),
            nSide = nSide,
            eSide = eSide,
            sSide = sSide,
            wSide = wSide
        )
        
        with open(self.outpath, "w") as file:
            file.write(json.dumps(cs, indent=4))
