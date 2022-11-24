from dataclasses import dataclass, field, asdict
import pandas as pd

# field mappings for bukken
bukkenRecordPath = "room"
bukkenMeta = ["tdfk", "shopHtmlName", "danchiNm", "traffic", "place", "floorAll"]
bukkenTrafficField = "traffic"
bukkenTrafficBus = "バス"
bukkenTrafficSep = "<br>"
bukkenNearestStationField = "nearestStation"
bukkenByWalkField = "byWalk"
bukkenByBusField = "byBus"
bukkenSystemField = "system"
bukkenHeaders = ["Todofuken", "Area", "Dan Chi Name", "Nearest Station", "Nearest station by Walk", "Nearest station by Bus", "Address", "Building Name", "Room Num", "Room Type", "Floor Space", "Floor", "Max Floor", "Rent", "Shikikin", "Common Fee", "System", "Room Link"]
bukkenColumns = ["tdfk", "shopHtmlName", "danchiNm", bukkenNearestStationField,bukkenByWalkField, bukkenByBusField, "place", "roomNmMain", "roomNmSub", "type", "floorspace", "floor", "floorAll", "rent", "shikikin", "commonfee", bukkenSystemField, "roomLinkPc"]

LIST_SEP = ","

# split traffic into by walk or by bus
def parse_traffic(x):
  nearestStationList = []
  byWalkList = []
  byBusList = []
  for traffic in str(x).split(bukkenTrafficSep):
    nearestStationList.append(traffic[:traffic.index("駅") + 1])
    if bukkenTrafficBus in traffic:
      byBusList.append(traffic)
    else:
      byWalkList.append(traffic)
  return [LIST_SEP.join(nearestStationList), LIST_SEP.join(byWalkList), LIST_SEP.join(byBusList)]

headers = [
  "city",
  "are",
  "traffic",
  "nearestStationByWalk",
  "nearestStationByBus",
  "address",
  "building",
  "room",
  "roomType",
  "floorSpace",
  "floor",
  "maxFloor",
  "rent",
  "commonFee",
  "total",
  "shikikin",
  "systems",
  "link",
  "city",
  "area",
  "traffic",
  "nearestStationByWalk",
  "nearestStationByBus",
  "address",
]

columns = [
  "city",
  "area",
  "traffic",
  "nearestStationByWalk",
  "nearestStationByBus",
  "address",
  "building",
  "room",
  "roomType",
  "floorSpace",
  "floor",
  "maxFloor",
  "rent",
  "commonFee",
  "total",
  "shikikin",
  "systems",
  "link",
  "city",
  "area",
  "traffic",
  "nearestStationByWalk",
  "nearestStationByBus",
  "address",
]

@dataclass
class Room:
    # building name
    building: str = ""
    room: str = ""
    roomType: str = ""
    floorSpace: float = 0
    floor: int = 0
    # top floor of building
    maxFloor: int = 0
    rent: int = 0
    commonFee: int = 0
    total: int = 0
    # shikikin requried
    shikikin: str = None
    # system
    systems: list = field(default_factory=list) 
    # link of room
    link: str = None

@dataclass
class Bukken:
    # todofuken
    city: str = ""
    # area of city
    area: str = ""
    # dan chi name
    danChi: str = ""
    # traffic of raw response
    traffic: str = ""
    # nearest station by walk
    nearestStationByWalk: str = ""
    # nearest station by bus
    nearestStationByBus: str = ""
    # address of building
    address: str = ""
    rooms: list[Room] = field(default_factory=list)

class Converter:
    def toRoom(self, json):
        return Room(
            building=json["roomNmMain"],
            room=json["roomNmSub"],
            roomType=json["type"],
            floorSpace=json["floorspace"],
            floor=json["floor"],
            rent=json["rent"],
            commonFee=json["commonfee"],
            shikikin=json["shikikin"],
            systems=json["system"],
            link="https://www.ur-net.go.jp" + json["roomLinkPc"],
        )

    def toBukken(self, json):
        # init base information of Bukken
        bukken = Bukken(
            city=json["tdfk"],
            area=json["shopHtmlName"],
            danChi=json["danchiNm"],
            traffic=json["traffic"],
            address=json["place"],
        )
        # TODO nearest station logic here
        for roomJson in json.get("room",[]):
            bukken.rooms.append(self.toRoom(roomJson))
        return bukken

    def toDf(self, bukken):
        df = pd.json_normalize(data=asdict(bukken), record_path="rooms", meta=[
            "city",
            "area",
            "traffic",
            "nearestStationByWalk",
            "nearestStationByBus",
            "address",
        ])
        if df.empty:
            return df
        # convert format
        toInt = lambda x : int("".join(c for c in x if c.isdigit()))
        df["floor"] = df["floor"].apply(lambda x: pd.Series(int(x[:len(x) - 1])))
        df["rent"] = df["rent"].apply(lambda x: pd.Series(toInt(x)))
        df["commonFee"] = df["commonFee"].apply(lambda x: pd.Series(toInt(x)))
        df["total"] = df["rent"] + df["commonFee"]
        df["floorSpace"] = df["floorSpace"].apply(lambda x: pd.Series(int(x.replace("&#13217;", ""))))
        df["systems"] = df["systems"].apply(lambda systems: pd.Series(str(list(map(lambda x: x["制度名"], systems)))))
        return df