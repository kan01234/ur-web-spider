from dataclasses import dataclass, field, asdict
import pandas as pd
from builder import RequestBuilder
import re

LIST_SEP = ","

# traffic column constant
BUKKEN_TRAFFIC_SEP = "<br>"
BUKKEN_TRAFFIC_REGEX_STATION_GROUP = "station"
BUKKEN_TRAFFIC_REGEX_BUS_GROUP = "bus"
BUKKEN_TRAFFIC_REGEX_WALK_GROUP = "walk"
BUKKEN_TRAFFIC_REGEX = f"(?P<{BUKKEN_TRAFFIC_REGEX_STATION_GROUP}>.*駅)[ ]?(バス(?P<{BUKKEN_TRAFFIC_REGEX_BUS_GROUP}>[0-9～]+)分)?[ ]?(徒歩(?P<{BUKKEN_TRAFFIC_REGEX_WALK_GROUP}>[0-9～]+)分)?"
BUKKEN_TRAFFIC_MINUTE_REGEX_FROM_GROUP = "from"
BUKKEN_TRAFFIC_MINUTE_REGEX_TO_GROUP = "to"
BUKKEN_TRAFFIC_MINUTE_REGEX = f"(?P<{BUKKEN_TRAFFIC_MINUTE_REGEX_FROM_GROUP}>[0-9]+)(～)?(?P<{BUKKEN_TRAFFIC_MINUTE_REGEX_TO_GROUP}>([0-9]+))?"

# room column constant
ROOM_FLOOR_COLUMN_NAME = "floor"
ROOM_FLOOR_SPACE_COLUMN_NAME = "floorSpace"
ROOM_RENT_COLUMN_NAME = "rent"
ROOM_TOTAL_COLUMN_NAME = "total"
ROOM_SHIKIKIN_COLUMN_NAME = "shikikin"
ROOM_TRAFFIC_COLUMN_NAME = "traffic"
ROOM_COMMON_FEE_COLUMN_NAME = "commonFee"
ROOM_SYSTEMS_COLUMN_NAME = "systems"

# station column constant
STATIONS_COLUMN_NAME = "stations"
STATION_NEAREST_STATION_BY_WALK_COLUMN_NAME = "nearestStationByWalk"
STATION_BEST_CASE_BY_WALK_COLUMN_NAME = "bestCaseByWalk"
STATION_WORST_CASE_BY_WALK_COLUMN_NAME = "worstCaseByWalk"
STATION_NEAREST_STATION_BY_BUS_COLUMN_NAME = "nearestStationByBus"
STATION_BEST_CASE_BY_BUS_COLUMN_NAME = "bestCaseByBus"
STATION_WORST_CASE_BY_BUS_COLUMN_NAME = "worstCaseByBus"

# bukken fields mappings
BUKKEN_RECORD_PATH = "rooms"
BUKKEN_CITY_COLUMN_NAME = "city"
BUKKEN_AREA_COLUMN_NAME = "area"
BUKKEN_DAN_CHI_COLUMN_NAME = "danChiName"
BUKKEN_ADDRESS_COLUMN_NAME = "address"
BUKKEN_META = [
    BUKKEN_CITY_COLUMN_NAME,
    BUKKEN_AREA_COLUMN_NAME,
    BUKKEN_DAN_CHI_COLUMN_NAME,
    ROOM_TRAFFIC_COLUMN_NAME,
    BUKKEN_ADDRESS_COLUMN_NAME,
]
bukkenFields = {
    "Todofuken": BUKKEN_CITY_COLUMN_NAME,
    "Area": BUKKEN_AREA_COLUMN_NAME,
    "Dan Chi Name": BUKKEN_DAN_CHI_COLUMN_NAME,
    "Nearest station by Walk": STATION_NEAREST_STATION_BY_WALK_COLUMN_NAME,
    "Best case by Walk": STATION_BEST_CASE_BY_WALK_COLUMN_NAME,
    "Worst case by Walk": STATION_WORST_CASE_BY_WALK_COLUMN_NAME,
    "Nearest station by Bus": STATION_NEAREST_STATION_BY_BUS_COLUMN_NAME,
    "Best case by Bus": STATION_BEST_CASE_BY_BUS_COLUMN_NAME,
    "Worst case by Bus": STATION_WORST_CASE_BY_BUS_COLUMN_NAME,
    "Traffic": ROOM_TRAFFIC_COLUMN_NAME,
    "Address": BUKKEN_ADDRESS_COLUMN_NAME,
    "Building Name": "buildingName",
    "Room Num": "room",
    "Room Type": "roomType",
    "Floor Space": ROOM_FLOOR_SPACE_COLUMN_NAME,
    "Floor": ROOM_FLOOR_COLUMN_NAME,
    "Max Floor": "maxFloor",
    "Rent": ROOM_RENT_COLUMN_NAME,
    "Common Fee": ROOM_COMMON_FEE_COLUMN_NAME,
    "Total Fee": ROOM_TOTAL_COLUMN_NAME,
    "Shikikin": ROOM_SHIKIKIN_COLUMN_NAME,
    "Systems": ROOM_SYSTEMS_COLUMN_NAME,
    "Room Link": "link"
}

@dataclass
class Station:
    # nearest station by walk
    nearestStationByWalk: str = None
    # best case by walk
    bestCaseByWalk: int = None
    # worst case by walk
    worstCaseByWalk: int = None
    # nearest station by bus
    nearestStationByBus: str = None
    # best case by bus
    bestCaseByBus: int = None
    # worst case by bus
    worstCaseByBus: int = None

@dataclass
class Room:
    # building name
    buildingName: str = ""
    # room
    room: str = ""
    # room type
    roomType: str = ""
    # floor space
    floorSpace: float = 0
    # floor
    floor: int = 0
    # stations json string
    stations: list[Station] = field(default_factory=list)
    # top floor of building
    maxFloor: int = 0
    # rent
    rent: int = 0
    # common fee
    commonFee: int = 0
    # total fee, rent + common fee
    total: int = 0
    # shikikin required
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
    danChiName: str = ""
    # traffic of raw response
    traffic: str = ""
    # address of building
    address: str = ""
    # list of rooms
    rooms: list[Room] = field(default_factory=list)

class Converter:
    def __init__(self, isDev = False):
        self.requestBuilder = RequestBuilder(isDev)

    def toRoom(self, json):
        room = Room(
            buildingName = json["roomNmMain"],
            room = json["roomNmSub"],
            roomType = json["type"],
            floorSpace = json["floorspace"],
            floor = json["floor"],
            rent = json["rent"],
            commonFee = json["commonfee"],
            shikikin = json["shikikin"],
            systems = json["system"],
            link = f"https://www.ur-net.go.jp{json['roomLinkPc']}",
        )
        return self.decorateDetail(room, json)

    def decorateDetail(self, room, json):
        response = self.requestBuilder.postRoomDetails(id=json["id"], shisya=json["shisya"], danchi=json["danchi"], shikibetu=json["shikibetu"])
        print(json["id"], json["shisya"], json["danchi"], json["shikibetu"])
        print(response==None)
        return room

    # convert traffic to station details
    def toStation(self, traffic: str):
        station = Station()
        trafficMatch = re.search(BUKKEN_TRAFFIC_REGEX, traffic)
        stationGroup = trafficMatch.group(BUKKEN_TRAFFIC_REGEX_STATION_GROUP)

        # bus
        busGroup = trafficMatch.group(BUKKEN_TRAFFIC_REGEX_BUS_GROUP)
        if busGroup is not None:
            station.nearestStationByBus = stationGroup
            busMatch = re.search(BUKKEN_TRAFFIC_MINUTE_REGEX, busGroup)
            bestCaseByBus = busMatch.group(BUKKEN_TRAFFIC_MINUTE_REGEX_FROM_GROUP)
            station.bestCaseByBus = bestCaseByBus
            worstCaseByBus = busMatch.group(BUKKEN_TRAFFIC_MINUTE_REGEX_TO_GROUP)
            if worstCaseByBus is not None:
                station.worstCaseByBus = worstCaseByBus

        # walk
        walkGroup = trafficMatch.group(BUKKEN_TRAFFIC_REGEX_WALK_GROUP)
        if walkGroup is not None:
            station.nearestStationByWalk = stationGroup
            walkMatch = re.search(BUKKEN_TRAFFIC_MINUTE_REGEX, walkGroup)
            bestCaseByWalk = walkMatch.group(BUKKEN_TRAFFIC_MINUTE_REGEX_FROM_GROUP)
            station.bestCaseByWalk = bestCaseByWalk
            worstCaseByWalk = walkMatch.group(BUKKEN_TRAFFIC_MINUTE_REGEX_TO_GROUP)
            if worstCaseByWalk is not None:
                station.worstCaseByWalk = worstCaseByWalk

        return station

    # convert traffic to station details
    def toStations(self, str: str):
        stations: list[Station] = []
        for traffic in str.split(BUKKEN_TRAFFIC_SEP):
            stations.append(self.toStation(traffic))

        return stations

    # station to df fields
    def toStationDf(self, station):
        return [station.nearestStationByWalk, station.bestCaseByWalk, station.worstCaseByWalk, station.nearestStationByBus, station.bestCaseByBus, station.bestCaseByWalk]

    # convert to bukken
    def toBukken(self, json):
        # init base information of Bukken
        bukken = Bukken(
            city = json["tdfk"],
            area = json["shopHtmlName"],
            danChiName = json["danchiNm"],
            traffic = json["traffic"],
            address = json["place"],
        )

        # convert traffic
        stations = self.toStations(json[ROOM_TRAFFIC_COLUMN_NAME])

        # convert room
        for roomJson in json.get("room",[]):
            room: Room = self.toRoom(roomJson)
            room.stations = stations
            bukken.rooms.append(room)
        return bukken

    # convert to data frame
    def toDf(self, bukken):
        df = pd.json_normalize(data=asdict(bukken), record_path=BUKKEN_RECORD_PATH, meta=BUKKEN_META)

        if df.empty:
            return df
        # convert format
        toInt = lambda x : int("".join(c for c in x if c.isdigit()))

        # floor to int, e.g. 5階 -> 5
        df[ROOM_FLOOR_COLUMN_NAME] = df[ROOM_FLOOR_COLUMN_NAME].apply(lambda x: pd.Series(int(x[:len(x) - 1])))

        # rent to int
        df[ROOM_RENT_COLUMN_NAME] = df[ROOM_RENT_COLUMN_NAME].apply(lambda x: pd.Series(toInt(x)))

        # common fee to int
        df[ROOM_COMMON_FEE_COLUMN_NAME] = df[ROOM_COMMON_FEE_COLUMN_NAME].apply(lambda x: pd.Series(toInt(x)))

        # total = rent + common fee
        df[ROOM_TOTAL_COLUMN_NAME] = df[ROOM_RENT_COLUMN_NAME] + df[ROOM_COMMON_FEE_COLUMN_NAME]

        # floor space to int, e.g. 48&#13217 -> 48
        df[ROOM_FLOOR_SPACE_COLUMN_NAME] = df[ROOM_FLOOR_SPACE_COLUMN_NAME].apply(lambda x: pd.Series(int(x.replace("&#13217;", ""))))

        # system name to list, e.g. [{'制度_IMG': 'btn_u35.png', '制度名': 'U35割', '制度HTML': 'u35'}] -> ["U35割"]
        df[ROOM_SYSTEMS_COLUMN_NAME] = df[ROOM_SYSTEMS_COLUMN_NAME].apply(lambda systems: pd.Series(str(list(map(lambda x: x["制度名"], systems)))))

        # station json array to different rows & columns
        df = df.explode(STATIONS_COLUMN_NAME).reset_index(drop=True)
        df = df.merge(pd.json_normalize(df[STATIONS_COLUMN_NAME]), left_index=True, right_index=True).drop(STATIONS_COLUMN_NAME, axis=1)

        return df