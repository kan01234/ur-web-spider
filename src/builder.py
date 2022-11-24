
import requests
import json

class RequestBuilder:
    BUKKEN_RESULT_URL = "https://chintai.sumai.ur-net.go.jp/chintai/api/bukken/result/bukken_result/"

    def postBukkenResult(self, block, tdfk, skcs, page, isDev = False):
        if (isDev):
            with open("./src/dev/bukkes-result-response.json", "r") as dummy:
                return json.loads(str(dummy.read()))
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
            "skcs": skcs,
            "block": block,
            "tdfk": tdfk,
            "rireki_tdfk": tdfk,
            "orderByField": 1,
            "pageSize": 10,
            "pageIndex": page,
            "shisya": None,
            "danchi": None,
            "shikibetu": None,
            "pageIndexRoom": 0,
            "sp": None
        }
        return json.loads(requests.post(BUKKEN_RESULT_URL, data=formBody, headers=headers).content.decode("utf-8"))
