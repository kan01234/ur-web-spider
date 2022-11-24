import pytest
from src.data import Converter, Station

@pytest.mark.parametrize("input,nearestStationByWalk,bestCaseByWalk,worstCaseByWalk,nearestStationByBus,bestCaseByBus,worstCaseByBus", [
    ("JR中央線「高尾」駅徒歩25～30分", "JR中央線「高尾」駅", "25", "30", None, None, None),
    ("JR中央線「高尾」駅バス7分 徒歩1～11分", "JR中央線「高尾」駅", "1", "11", "JR中央線「高尾」駅", "7", None),
    ("JR中央線ほか｢八王子｣駅 徒歩13分", "JR中央線ほか｢八王子｣駅", "13", None, None, None, None),
    ("多摩都市モノレール「松が谷」駅 徒歩5～8分", "多摩都市モノレール「松が谷」駅", "5", "8", None, None, None),
    ("京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅バス5分 徒歩2～4分", "京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅", "2", "4", "京王相模原線「京王多摩センター」駅・小田急多摩線「小田急多摩センター」駅・多摩都市モノレール「多摩センター」駅", "5", None),
    ("JR中央本線「高尾」駅 徒歩29～38分", "JR中央本線「高尾」駅", "29", "38", None, None, None),
    ("JR中央線「高尾」駅バス7分 徒歩1～11分", "JR中央線「高尾」駅", "1", "11", "JR中央線「高尾」駅", "7", None),
    ("京王高尾線「高尾」駅バス7分 徒歩1～11分", "京王高尾線「高尾」駅", "1", "11", "京王高尾線「高尾」駅", "7", None),
])
def testToStation(input, nearestStationByWalk, bestCaseByWalk, worstCaseByWalk, nearestStationByBus, bestCaseByBus, worstCaseByBus):
    converter = Converter()
    station: Station = converter.toStation(input)
    assert nearestStationByWalk == station.nearestStationByWalk
    assert bestCaseByWalk == station.bestCaseByWalk
    assert worstCaseByWalk == station.worstCaseByWalk
    assert nearestStationByBus == station.nearestStationByBus
    assert bestCaseByBus == station.bestCaseByBus
    assert worstCaseByBus == station.worstCaseByBus