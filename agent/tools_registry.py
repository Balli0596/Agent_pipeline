
from langchain.tools import tool

from tools.weather_tools import get_weather as fetch_weather
from tools.stock_tools import get_stock_price as fetch_stock_price


@tool
def weather_tool(city: str) -> dict:
    """Get the current weather, temperature, humidity and wind speed for a city."""
    return fetch_weather(city)


@tool
def stock_tool(symbol: str) -> dict:
    """Get the latest available closing stock price for a ticker symbol."""
    return fetch_stock_price(symbol)


TOOLS = [weather_tool, stock_tool]
