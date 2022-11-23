import requests
import json
from datetime import datetime
import yaml
import pandas as pd

try:
  configFile = yaml.safe_load(open("./config.yaml", "rb"))
  isDev=configFile.get("isDev")
except:
  print("use default config")
  isDev=False


BUKKEN_RESULT_URL = "https://chintai.sumai.ur-net.go.jp/chintai/api/bukken/result/bukken_result/"
OUTPUT_FILE_NAME = "bukken-" + datetime.now().strftime("%Y%m%dT%H%M")

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
bukkenMeta = ["danchiNm", "traffic", "place", "floorAll"]

# open file write stream
jsonRowCount = -1
with open(OUTPUT_FILE_NAME + ".json", "w") as jsonFile, open(OUTPUT_FILE_NAME + ".csv", "w") as csvFile:
  hasNextPage = True
  page=0
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
      data_frame = pd.json_normalize(bukken, bukkenRecordPath, bukkenMeta)
      if not data_frame.empty:
        csvFile.write(data_frame.to_csv(index=False))

    # TODO hasNextPage = len(responseData) >= 0
    hasNextPage = False
    formBody["pageIndex"] += 1
  jsonFile.write("\n]\n")
