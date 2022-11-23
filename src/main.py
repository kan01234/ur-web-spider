import requests
import json

# details url
BUKKEN_RESULT_URL = "https://chintai.sumai.ur-net.go.jp/chintai/api/bukken/result/bukken_result/"

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

hasNextPage = True
page=0
while hasNextPage:
  response = requests.post(BUKKEN_RESULT_URL, data=formBody, headers=headers)
  responseData = json.loads(response.content)
  # TODO write to csv or something
  hasNextPage = len(responseData) >= 0
  # TODO update form body
  formBody["pageIndex"] += 1
