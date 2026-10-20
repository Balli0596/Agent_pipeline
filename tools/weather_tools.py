
import requests


def get_weather(city: str) -> dict:
    """Get current weather for a city."""

    try:
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en"},
            timeout=10,
        )
        geo_response.raise_for_status()
        locations = geo_response.json().get("results", [])

        if not locations:
            return {"error": f"City not found: {city}"}

        location = locations[0]

        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,wind_speed_10m,weather_code"
                ),
            },
            timeout=10,
        )
        weather_response.raise_for_status()

        return {
            "city": location["name"],
            "country": location.get("country", ""),
            "current_weather": weather_response.json().get("current", {}),
        }

    except requests.RequestException as exc:
        return {"error": f"Weather service unavailable: {exc}"}
