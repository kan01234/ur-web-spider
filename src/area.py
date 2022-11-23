from bs4 import BeautifulSoup
import requests

AREA_URL="https://www.ur-net.go.jp/chintai/"

def areaMap():
    page = requests.get(AREA_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = {}
    shapes = soup.find("map", attrs={"name": "map_gnav"}).find_all("area", attrs={"shape": "rect"})
    for shape in shapes:
        name = shape["alt"]
        code = shape["key-code"]
        results[code] = name
    return results

# print(areaMap())