
from tools.weather_tools import get_weather
from tools.stock_tools import get_stock_price


def test_weather():
    result = get_weather("Jaipur")
    assert "error" not in result, result
    assert "current_weather" in result


def test_stock():
    result = get_stock_price("TCS.NS")
    assert "error" not in result, result
    assert result["latest_close"] > 0
