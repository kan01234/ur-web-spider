from bs4 import BeautifulSoup
import requests

AREA_URL="https://www.ur-net.go.jp/chintai/{area}/{city}/area/"

def skcsList(area, city):
    page = requests.get(AREA_URL.format(area = area, city = city))
    soup = BeautifulSoup(page.text, "html.parser")
    checkboxes = soup.find_all("li", attrs={"class": "item_list js-searchMain"})
    results = []
    for checkbox in checkboxes:
        code = checkbox.find("input", attrs={"name": "skcs"})['value']
        results.append(code)
