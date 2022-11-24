from dataclasses import dataclass, field
from pandas_dataclasses import AsFrame, Data, Index

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
class Bukken(AsFrame):
    # todofuken
    city: Index[str] = ""
    # area of city
    area: Index[str] = ""
    # dan chi name
    danChi: Data[str] = ""
    # traffic of raw response
    traffic: Data[str] = ""
    # nearest station by walk
    nearestStationByWalk: Data[str] = ""
    # nearest station by bus
    nearestStationByBus: Data[str] = ""
    # address of building
    address: Data[str] = ""
    rooms: Data[list[Room]] = field(default_factory=list)
