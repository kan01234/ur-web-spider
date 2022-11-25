
import traceback
import json
from datetime import datetime
import yaml
from data import Converter, BUKKEN_FIELDS
from builder import RequestBuilder
import os

try:
  configFile = yaml.safe_load(open("./config.yaml", "rb"))
  isDev=configFile.get("isDev")
  queries = configFile.get("queries")
  outputDirectory = configFile.get("output")["directory"]
except:
  print("use default config")
  isDev=False

# mkdir if not exist
if (not os.path.exists(outputDirectory)):
  os.mkdir(outputDirectory)

OUTPUT_FILE_NAME = outputDirectory + "bukken-" + datetime.now().strftime("%Y%m%d")

requestBuilder = RequestBuilder(isDev)
# open file write stream
jsonRowCount = -1

with open(OUTPUT_FILE_NAME + ".json", "w") as jsonFile, open(OUTPUT_FILE_NAME + ".csv", "w") as csvFile:
  showHeader = True
  hasNextPage = True
  converter = Converter(isDev)
  jsonFile.write("[")
  for block, values in queries.items():
    for tdfk, skcsStr in values.items():
      for skcs in skcsStr.split(","):
        print("fetching", block, tdfk, skcs)
        page=-1
        try:
          while hasNextPage:
            page+=1
            bukkens = requestBuilder.postBukkenResult(block=block, tdfk=tdfk, skcs=skcs, page=page)
            if (bukkens == None or len(bukkens) == 0 or int(bukkens[0]["roomCount"]) == 0):
              break
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
                path_or_buf = csvFile,
                header = BUKKEN_FIELDS.keys() if showHeader else False,
                columns = BUKKEN_FIELDS.values(),
                encoding = "utf-8",
                index = False,
              )
              showHeader = False
            hasNextPage = len(bukkens) >= 0 or not isDev
        except Exception as e:
          print(f"[error] on handling bukken {block} {tdfk} {skcs} {page}")
          traceback.print_exc()
  jsonFile.write("\n]\n")
