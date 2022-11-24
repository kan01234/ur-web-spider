from dataclasses import dataclass, field, asdict
import pandas as pd

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
            roomType=json["floorspace"],
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
        return pd.json_normalize(data=asdict(bukken), record_path="rooms", meta=[
            "city",
            "area",
            "traffic",
            "nearestStationByWalk",
            "nearestStationByBus",
            "address",
        ])