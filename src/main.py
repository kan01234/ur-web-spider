from dataclasses import asdict
import requests
import json
from datetime import datetime
import yaml
import pandas as pd
import re
from model import Bukken, Room

try:
  configFile = yaml.safe_load(open("./config.yaml", "rb"))
  isDev=configFile.get("isDev")
except:
  print("use default config")
  isDev=False


BUKKEN_RESULT_URL = "https://chintai.sumai.ur-net.go.jp/chintai/api/bukken/result/bukken_result/"
OUTPUT_FILE_NAME = "bukken-" + datetime.now().strftime("%Y%m%d")

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

formBody = {
    "rent_low": None,
    "rent_high": None,
    "walk": None,
    "floorspace_low": None,
    "floorspace_high": None,
    "years": None,
    "mode": "area",
    "skcs": 201,
    "skcs": 201,
    "block": "kanto",
    "tdfk": 13,
    "rireki_tdfk": 13,
    "orderByField": 1,
    "pageSize": 10,
    "pageIndex": 0,
    "shisya": None,
    "danchi": None,
    "shikibetu": None,
    "pageIndexRoom": 0,
    "sp": None
}

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
bukkenSystemNameField = "制度名"
bukkenHeaders = ["Todofuken", "Area", "Dan Chi Name", "Nearest Station", "Nearest station by Walk", "Nearest station by Bus", "Address", "Building Name", "Room Num", "Room Type", "Floor Space", "Floor", "Max Floor", "Rent", "Shikikin", "Common Fee", "System", "Room Link"]
bukkenColumns = ["tdfk", "shopHtmlName", "danchiNm", bukkenNearestStationField,bukkenByWalkField, bukkenByBusField, "place", "roomNmMain", "roomNmSub", "type", "floorspace", "floor", "floorAll", "rent", "shikikin", "commonfee", bukkenSystemField, "roomLinkPc"]

LIST_SEP = ","

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

# flatten system json value
def parse_system(x):
  return LIST_SEP.join(pd.json_normalize(x)[bukkenSystemNameField])

# open file write stream
jsonRowCount = -1
with open(OUTPUT_FILE_NAME + ".json", "w") as jsonFile, open(OUTPUT_FILE_NAME + ".csv", "w") as csvFile:
  hasNextPage = True
  jsonFile.write("[")
  while hasNextPage:
    if (isDev):
      with open("./src/dev/bukkes-result-response.json", "r") as dummy:
        response = str(dummy.read())
    else:
      response = requests.post(BUKKEN_RESULT_URL, data=formBody, headers=headers).content.decode("utf-8")
    bukkens = json.loads(response)
    for bukkenJson in bukkens:
      jsonRowCount += 1
      # write to json file
      if (jsonRowCount == 0):
        jsonFile.write("\n  " + json.dumps(bukkenJson))
      else:
        jsonFile.write(",\n  " + json.dumps(bukkenJson))
      
      # init base information of Bukken
      bukken = Bukken(
        city=bukkenJson["tdfk"],
        area=bukkenJson["shopHtmlName"],
        danChi=bukkenJson["danchiNm"],
        traffic=bukkenJson["traffic"],
        address=bukkenJson["place"],
      )

      # TODO nearest station logic here


      for roomJson in bukkenJson.get("room",[]):
        room = Room(
          building=roomJson["roomNmMain"],
          room=roomJson["roomNmSub"],
          roomType=roomJson["floorspace"],
          floor=roomJson["floor"],
          rent=roomJson["rent"],
          commonFee=roomJson["commonfee"],
          shikikin=roomJson["shikikin"],
          systems=roomJson["system"],
          link="https://www.ur-net.go.jp" + roomJson["roomLinkPc"],
        )
        bukken.rooms.append(room)

      # continue if no rooms available
      if (len(bukken.rooms) <= 0):
        continue
      df = pd.json_normalize(asdict(bukken), "rooms", [
        "city",
        "area",
        "traffic",
        "nearestStationByWalk",
        "nearestStationByBus",
        "address",
      ])
      df.to_csv(
        path_or_buf=csvFile,
        header=headers,
        columns=columns,
        encoding="utf-8",
      )

      headers = False
    # TODO hasNextPage = len(responseData) >= 0
    hasNextPage = False
    formBody["pageIndex"] += 1
  jsonFile.write("\n]\n")
