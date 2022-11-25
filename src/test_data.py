import pytest
from src.data import Converter, Station

@pytest.mark.parametrize("input,nearestStationByWalk,bestCaseByWalk,worstCaseByWalk,nearestStationByBus,bestCaseByBus,worstCaseByBus", [
    ("JR中央線「高尾」駅徒歩25～30分", "JR中央線「高尾」駅", 25, 30, None, None, None),
    ("JR中央線「高尾」駅バス7分 徒歩1～11分", None, None, None, "JR中央線「高尾」駅", 8, 18),
    ("JR中央線ほか｢八王子｣駅 徒歩13分", "JR中央線ほか｢八王子｣駅", 13, 13, None, None, None),
    ("多摩都市モノレール「松が谷」駅 徒歩5～8分", "多摩都市モノレール「松が谷」駅", 5, 8, None, None, None),
    ("京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅バス5分 徒歩2～4分", None, None, None, "京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅", 7, 9),
    ("JR中央本線「高尾」駅 徒歩29～38分", "JR中央本線「高尾」駅", 29, 38, None, None, None),
    ("JR中央線「高尾」駅バス7分 徒歩1～11分", None, None, None, "JR中央線「高尾」駅", 8, 18),
    ("京王高尾線「高尾」駅バス7分 徒歩1～11分", None, None, None, "京王高尾線「高尾」駅", 8, 18),
    ("京成本線「八千代台」駅バス7～8分 徒歩1～11分", None, None, None, "京成本線「八千代台」駅", 8, 19),
    ("JR根岸線・横浜市営地下鉄ブルーライン「桜木町」バス26分徒歩1分", None, None, None, "JR根岸線・横浜市営地下鉄ブルーライン「桜木町」", 27, 27),
    ("JR根岸線・横浜市営地下鉄ブルーライン「桜木町」徒歩1分", "JR根岸線・横浜市営地下鉄ブルーライン「桜木町」", 1, 1, None, None, None),
])
def testToStation(input, nearestStationByWalk, bestCaseByWalk, worstCaseByWalk, nearestStationByBus, bestCaseByBus, worstCaseByBus):
    converter = Converter(True)
    station: Station = converter.toStation(input)
    assert nearestStationByWalk == station.nearestStationByWalk
    assert bestCaseByWalk == station.bestCaseByWalk
    assert worstCaseByWalk == station.worstCaseByWalk
    assert nearestStationByBus == station.nearestStationByBus
    assert bestCaseByBus == station.bestCaseByBus
    assert worstCaseByBus == station.worstCaseByBus

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
            Station("JR中央線「高尾」駅", 1, 30, "JR中央線「高尾」駅", 8, 24),
            Station("JR中央線ほか｢八王子｣駅", 13, 13, None, None, None),
            Station("多摩都市モノレール「松が谷」駅", 5, 8, None, None, None),
            Station(None, None, None, "京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅", 7, 9),
            Station("JR中央本線「高尾」駅", 29, 38, None, None, None),
            Station(None, None, None, "京王高尾線「高尾」駅", 8, 18),
            Station(None, None, None, "京成本線「八千代台」駅", 8, 19),
            Station("JR根岸線・横浜市営地下鉄ブルーライン「桜木町」", 1, 1, "JR根岸線・横浜市営地下鉄ブルーライン「桜木町」", 27, 27),
    ]),
])
def testToStations(input, expectedStations):
    converter = Converter(True)
    stations: list[Station] = converter.toStations(input)
    assert expectedStations == stations