import pytest
from src.data import Converter, Station, StationDetail


# for debug
# JR中央線「高尾」駅徒歩25～30分
# JR中央線「高尾」駅バス7分 徒歩1～11分
# JR中央線ほか｢八王子｣駅 徒歩13分
# 多摩都市モノレール「松が谷」駅 徒歩5～8分
# 京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅バス5分 徒歩2～4分
# JR中央本線「高尾」駅 徒歩29～38分
# JR中央線「高尾」駅バス7分 徒歩1～11分
# 京王高尾線「高尾」駅バス7分 徒歩1～11分
# 京成本線「八千代台」駅バス7～8分 徒歩1～11分
# JR根岸線・横浜市営地下鉄ブルーライン「桜木町」バス26分徒歩1分
# JR根岸線・横浜市営地下鉄ブルーライン「桜木町」徒歩1分
# 京王相模原線「南大沢」駅（3－1～3号棟）徒歩8分 またはバス3分 徒歩4分、（16－1～5号棟）徒歩15～17分 またはバス8分 徒歩3～4分
# 京王線「聖蹟桜ヶ丘」駅（3－1～3号棟）バス37分 徒歩3～4分、（16－1～5号棟）バス37分 徒歩12～13分
# つくばエクスプレス「北千住」駅 徒歩5～7分
@pytest.mark.parametrize("input,expectedStation", [
    ("JR中央線「高尾」駅徒歩25～30分", Station(StationDetail("JR中央線「高尾」駅", 25, 30), StationDetail())),
    ("JR中央線「高尾」駅バス7分 徒歩1～11分", Station(StationDetail(), StationDetail("JR中央線「高尾」駅", 8, 18))),
    ("JR中央線ほか｢八王子｣駅 徒歩13分", Station(StationDetail("JR中央線ほか｢八王子｣駅", 13, 13), StationDetail())),
    ("多摩都市モノレール「松が谷」駅 徒歩5～8分", Station(StationDetail("多摩都市モノレール「松が谷」駅", 5, 8), StationDetail())),
    ("京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅バス5分 徒歩2～4分", Station(StationDetail(), StationDetail("京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅", 7, 9))),
    ("JR中央本線「高尾」駅 徒歩29～38分", Station(StationDetail("JR中央本線「高尾」駅", 29, 38), StationDetail())),
    ("JR中央線「高尾」駅バス7分 徒歩1～11分", Station(StationDetail(), StationDetail("JR中央線「高尾」駅", 8, 18))),
    ("京王高尾線「高尾」駅バス7分 徒歩1～11分", Station(StationDetail(), StationDetail("京王高尾線「高尾」駅", 8, 18))),
    ("京成本線「八千代台」駅バス7～8分 徒歩1～11分", Station(StationDetail(), StationDetail("京成本線「八千代台」駅", 8, 19))),
    ("JR根岸線・横浜市営地下鉄ブルーライン「桜木町」バス26分徒歩1分", Station(StationDetail(), StationDetail("JR根岸線・横浜市営地下鉄ブルーライン「桜木町」", 27, 27))),
    ("JR根岸線・横浜市営地下鉄ブルーライン「桜木町」徒歩1分", Station(StationDetail("JR根岸線・横浜市営地下鉄ブルーライン「桜木町」", 1, 1), StationDetail())),
    ("京王相模原線「南大沢」駅（3－1～3号棟）徒歩8分 またはバス3分 徒歩4分、（16－1～5号棟）徒歩15～17分 またはバス8分 徒歩3～4分", Station(StationDetail("京王相模原線「南大沢」駅", 8, 17), StationDetail("京王相模原線「南大沢」駅", 7, 12))),
    ("京王線「聖蹟桜ヶ丘」駅（3－1～3号棟）バス37分 徒歩3～4分、（16－1～5号棟）バス37分 徒歩12～13分", Station(StationDetail(), StationDetail("京王線「聖蹟桜ヶ丘」駅", 40, 50))),
    ("つくばエクスプレス「北千住」駅 徒歩5～7分", Station(StationDetail("つくばエクスプレス「北千住」駅", 5, 7), StationDetail()))
])
def testToStation(input, expectedStation):
    converter = Converter(True)
    station: Station = converter.toStation(input)
    assert expectedStation == station


@pytest.mark.parametrize("input,expectedStations", [(
    "JR中央線「高尾」駅徒歩25～30分<br>"
    + "JR中央線「高尾」駅バス7分 徒歩1～11分<br>"
    + "JR中央線ほか｢八王子｣駅 徒歩13分<br>"
    + "多摩都市モノレール「松が谷」駅 徒歩5～8分<br>"
    + "京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅バス5分 徒歩2～4分<br>"
    + "JR中央本線「高尾」駅 徒歩29～38分<br>"
    + "JR中央線「高尾」駅バス7分 徒歩5～17分<br>"
    + "京王高尾線「高尾」駅バス7分 徒歩1～11分<br>"
    + "京成本線「八千代台」駅バス7～8分 徒歩1～11分<br>"
    + "JR根岸線・横浜市営地下鉄ブルーライン「桜木町」バス26分徒歩1分<br>"
    + "JR根岸線・横浜市営地下鉄ブルーライン「桜木町」徒歩1分<br>"
    + "JR中央線「高尾」駅徒歩1～20分", [
        Station(StationDetail("JR中央線「高尾」駅", 1, 30), StationDetail("JR中央線「高尾」駅", 8, 24)),
        Station(StationDetail("JR中央線ほか｢八王子｣駅", 13, 13), StationDetail()),
        Station(StationDetail("多摩都市モノレール「松が谷」駅", 5, 8), StationDetail()),
        Station(StationDetail(), StationDetail("京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅", 7, 9)),
        Station(StationDetail("JR中央本線「高尾」駅", 29, 38), StationDetail()),
        Station(StationDetail(), StationDetail("京王高尾線「高尾」駅", 8, 18)),
        Station(StationDetail(), StationDetail("京成本線「八千代台」駅", 8, 19)),
        Station(StationDetail("JR根岸線・横浜市営地下鉄ブルーライン「桜木町」", 1, 1), StationDetail("JR根岸線・横浜市営地下鉄ブルーライン「桜木町」", 27, 27)),
    ]),
])
def testToStations(input, expectedStations):
    converter = Converter(True)
    stations: list[Station] = converter.toStations(input)
    assert expectedStations == stations
