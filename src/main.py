
import requests
import json
from datetime import datetime
import yaml
import re
from data import Converter, headers, columns

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

# open file write stream
jsonRowCount = -1
with open(OUTPUT_FILE_NAME + ".json", "w") as jsonFile, open(OUTPUT_FILE_NAME + ".csv", "w") as csvFile:
  hasNextPage = True
  converter = Converter()
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

      df = converter.toDf(converter.toBukken(bukkenJson))
      # skip if df is empty
      if df.empty:
        continue
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
