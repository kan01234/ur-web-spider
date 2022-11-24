from dataclasses import dataclass, field

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
