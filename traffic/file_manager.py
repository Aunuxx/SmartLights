import json
from SmartLights.traffic import Light

class FileManager:
    def __init__(self) -> None:
        self.outpath = "currentstate.json"

    def readFile(self) -> dict[str, list[dict[str, int]]]:
        with open(self.outpath, "r") as file:
            return dict(json.load(file))
        return {}

    def getData(self, id: int, key: str) -> int:
        return self.readFile()["Lights"][id][key]

    def setData(self, id: int, key: str, data: int) -> None:
        cs = self.readFile()["Lights"][id][key] = data
        with open(self.outpath, "w") as file:
            file.write(json.dumps(cs, indent=4))

    def getLight(self, id: int) -> Light:
        cs = self.readFile()["Lights"][id]
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

    def writeLight(self, light: Light) -> None:
        cs = self.readFile()

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
