
import requests
import json
from datetime import datetime
import yaml
import re
from data import Converter, headers, columns
from builder import RequestBuilder

try:
  configFile = yaml.safe_load(open("./config.yaml", "rb"))
  isDev=configFile.get("isDev")
except:
  print("use default config")
  isDev=False

OUTPUT_FILE_NAME = "bukken-" + datetime.now().strftime("%Y%m%d")

requestBuilder = RequestBuilder()
# open file write stream
jsonRowCount = -1
with open(OUTPUT_FILE_NAME + ".json", "w") as jsonFile, open(OUTPUT_FILE_NAME + ".csv", "w") as csvFile:
  hasNextPage = True
  converter = Converter()
  jsonFile.write("[")
  page=-1
  while hasNextPage:
    page+=1
    bukkens = requestBuilder.postBukkenResult(block="kanto", tdfk=13, skcs=201, page=page, isDev=isDev)
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
        index=False,
      )

      headers = False
    # TODO hasNextPage = len(responseData) >= 0
    hasNextPage = False
  jsonFile.write("\n]\n")
