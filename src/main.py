import requests
import json
from datetime import datetime
import yaml
import pandas as pd
import re

try:
  configFile = yaml.safe_load(open("./config.yaml", "rb"))
  isDev=configFile.get("isDev")
except:
  print("use default config")
  isDev=False


BUKKEN_RESULT_URL = "https://chintai.sumai.ur-net.go.jp/chintai/api/bukken/result/bukken_result/"
OUTPUT_FILE_NAME = "bukken-" + datetime.now().strftime("%Y%m%dT")

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
bukkenHeaders = ["Todofuken", "Area", "Dan Chi Name", "Nearest Station", "Nearest station by Walk", "Nearest station by Bus", "Address", "Building Name", "Room Num", "Room Type", "Floor Space", "Floor", "Max Floor", "Rent", "Shikikin", "Common Fee", "System", "Madori", "Room Link"]
bukkenColumns = ["tdfk", "shopHtmlName", "danchiNm", bukkenNearestStationField,bukkenByWalkField, bukkenByBusField, "place", "roomNmMain", "roomNmSub", "type", "floorspace", "floor", "floorAll", "rent", "shikikin", "commonfee", bukkenSystemField, "madori", "roomLinkPc"]

list_sep = ","

# split traffic into by walk or by bus
def parse_traffic(x):
  stations = []
  by_walk = []
  by_bus = []
  for traffic in str(x).split(bukkenTrafficSep):
    stations.append(re.search("(.*)(「.*」)(駅)", traffic)[0])
    if bukkenTrafficBus in traffic:
      by_bus.append(traffic)
    else:
      by_walk.append(traffic)
  return [list_sep.join(stations), list_sep.join(by_walk), list_sep.join(by_bus)]

# flatten system json value
def parse_system(x):
  return list_sep.join(pd.json_normalize(x)[bukkenSystemNameField])

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
    for bukken in bukkens:
      jsonRowCount += 1
      # write to json file
      if (jsonRowCount == 0):
        jsonFile.write("\n  " + json.dumps(bukken))
      else:
        jsonFile.write(",\n  " + json.dumps(bukken))
      
      # to csv
      df = pd.json_normalize(bukken, bukkenRecordPath, bukkenMeta)
      if not df.empty:
        df[[bukkenNearestStationField, bukkenByWalkField, bukkenByBusField]] = df[bukkenTrafficField].apply(lambda x: pd.Series(parse_traffic(str(x))))
        df[bukkenSystemField] = df[bukkenSystemField].apply(lambda x: pd.Series(parse_system(x)))
        df.to_csv(
          path_or_buf=csvFile,
          index=False,
          header=bukkenHeaders,
          columns=bukkenColumns,
          encoding="utf-8"
        )
      bukkenHeaders = False
    # TODO hasNextPage = len(responseData) >= 0
    hasNextPage = False
    formBody["pageIndex"] += 1
  jsonFile.write("\n]\n")
