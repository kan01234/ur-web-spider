import requests
import json
from datetime import datetime

BUKKEN_RESULT_URL = "https://chintai.sumai.ur-net.go.jp/chintai/api/bukken/result/bukken_result/"
OUTPUT_FILE_NAME = "bukken-" + datetime.now().strftime("%Y%m%dT%H%M") + ".csv"

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
with open(OUTPUT_FILE_NAME, "w") as file:
  hasNextPage = True
  page=0
  while hasNextPage:
    response = requests.post(BUKKEN_RESULT_URL, data=formBody, headers=headers)
    # print(response.content.decode("utf-8"))
    bukkens = json.loads(response.content.decode("utf-8"))
    for bukken in bukkens:
      # TODO convert format
      # TODO write to csv or something
      print(str(bukken))

    # TODO hasNextPage = len(responseData) >= 0
    hasNextPage = False
    formBody["pageIndex"] += 1
