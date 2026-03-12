"""
HW 4: Open-Meteo Weather Utility
Benjamin Adovasio
API documentation: https://open-meteo.com/en/docs

Description:
    This utility fetches current weather conditions from the Open-Meteo
    Forecast API. You provide a latitude and longitude on the command line,
    and the script prints a small weather report for that location.

How to run:
    python3 hw4.py --lat 44.1004 --lon -70.2148
    python3 hw4.py --lat 44.1004 --lon -70.2148 --temp-unit fahrenheit --wind-unit mph
    python3 hw4.py --lat 44.1004 --lon -70.2148 --timezone America/New_York
"""

import sys
from typing import Dict, List, Optional


BASE_URL = "https://api.open-meteo.com/v1/forecast"
CURRENT_FIELDS = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "is_day",
    "precipitation",
    "weather_code",
    "cloud_cover",
    "wind_speed_10m",
    "wind_direction_10m",
]

#weather codes coppied from api docs
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def print_help() -> None:
    """Print a help message describing how to use the utility."""
    print(
        """Open-Meteo Weather Utility

Usage:
    python3 hw4.py --lat LATITUDE --lon LONGITUDE [options]

Required arguments:
    --lat LATITUDE          Latitude for the weather lookup (-90 to 90)
    --lon LONGITUDE         Longitude for the weather lookup (-180 to 180)

Optional arguments found via api docs:
    --temp-unit UNIT        celsius or fahrenheit (default: celsius)
    --wind-unit UNIT        kmh, ms, mph, or kn (default: kmh)
    --timezone ZONE         Time zone name or auto (default: auto)
    --help                  Show this help message
"""
    )


def parse_args(argv: List[str]) -> Optional[Dict[str, str]]:
    """Parse command-line arguments using sys.argv-style input."""
    if not argv or "--help" in argv:
        print_help()
        return None

    option_map = {
        "--lat": "latitude",
        "--lon": "longitude",
        "--temp-unit": "temperature_unit",
        "--wind-unit": "wind_speed_unit",
        "--timezone": "timezone",
    }

    parsed = {
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "timezone": "auto",
    }

    index = 0
    while index < len(argv):
        flag = argv[index]

        if flag not in option_map:
            raise ValueError(f"Unknown argument: {flag}")

        if index + 1 >= len(argv):
            raise ValueError(f"Missing value after {flag}")

        parsed[option_map[flag]] = argv[index + 1]
        index += 2

    if "latitude" not in parsed or "longitude" not in parsed:
        raise ValueError("You must provide both --lat and --lon.")

    try:
        latitude = float(parsed["latitude"])
        longitude = float(parsed["longitude"])
    except ValueError as err:
        raise ValueError("Latitude and longitude must be numbers.") from err

    if not -90 <= latitude <= 90:
        raise ValueError("Latitude must be between -90 and 90.")

    if not -180 <= longitude <= 180:
        raise ValueError("Longitude must be between -180 and 180.")

    if parsed["temperature_unit"] not in {"celsius", "fahrenheit"}:
        raise ValueError("Temperature unit must be celsius or fahrenheit.")

    if parsed["wind_speed_unit"] not in {"kmh", "ms", "mph", "kn"}:
        raise ValueError("Wind unit must be kmh, ms, mph, or kn.")

    parsed["latitude"] = str(latitude)
    parsed["longitude"] = str(longitude)
    return parsed


def weather_description(code: int) -> str:
    """Return a readable weather description for an Open-Meteo WMO code."""
    return WEATHER_CODES.get(code, "Unknown weather condition")


def fetch_weather(query_options: Dict[str, str]) -> Dict:
    """Send the GET request to Open-Meteo and return the JSON response."""
    try:
        import requests
    except ModuleNotFoundError as err:
        raise RuntimeError(
            "The requests library is not installed. Install it with: "
            "python3 -m pip install requests"
        ) from err

    # Open-Meteo parameters used in this utility:
    # - latitude / longitude: required coordinates for the requested location.
    # - current: tells the API which current-condition fields to include.
    # - temperature_unit: lets the user choose Celsius or Fahrenheit.
    # - wind_speed_unit: lets the user choose km/h, m/s, mph, or knots.
    # - timezone: returns times in the requested zone, or auto-detects the zone.
    params = {
        "latitude": query_options["latitude"],
        "longitude": query_options["longitude"],
        "current": ",".join(CURRENT_FIELDS),
        "temperature_unit": query_options["temperature_unit"],
        "wind_speed_unit": query_options["wind_speed_unit"],
        "timezone": query_options["timezone"],
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise ConnectionError(f"Request failed: {err}") from err

    payload = response.json()
    if payload.get("error"):
        raise ValueError(payload.get("reason", "The API returned an unknown error."))

    return payload


def display_weather_report(payload: Dict) -> None:
    """Print a readable weather report from the API response."""
    current = payload["current"]
    units = payload["current_units"]
    code = current["weather_code"]
    daylight = "Day" if current["is_day"] == 1 else "Night"

    print("Open-Meteo Weather Report")
    print(f"Coordinates: {payload['latitude']}, {payload['longitude']}")
    print(f"Timezone: {payload['timezone']}")
    print(f"Observed at: {current['time']}")
    print(f"Condition: {weather_description(code)} (WMO code {code})")
    print(f"Day/Night: {daylight}")
    print(f"Temperature: {current['temperature_2m']} {units['temperature_2m']}")
    print(
        f"Feels like: {current['apparent_temperature']} "
        f"{units['apparent_temperature']}"
    )
    print(
        f"Humidity: {current['relative_humidity_2m']} "
        f"{units['relative_humidity_2m']}"
    )
    print(f"Precipitation: {current['precipitation']} {units['precipitation']}")
    print(f"Cloud cover: {current['cloud_cover']} {units['cloud_cover']}")
    print(
        f"Wind: {current['wind_speed_10m']} {units['wind_speed_10m']} "
        f"at {current['wind_direction_10m']} {units['wind_direction_10m']}"
    )


def main() -> int:
    """Coordinate argument parsing, API access, and report output."""
    try:
        query_options = parse_args(sys.argv[1:])
        if query_options is None:
            return 0

        payload = fetch_weather(query_options)
        display_weather_report(payload)
        return 0

    except ValueError as err:
        print(f"Error: {err}")
        print()
        print_help()
        return 1

    except RuntimeError as err:
        print(err)
        return 1

    except ConnectionError as err:
        print(err)
        return 1

    except KeyError as err:
        print(f"Unexpected API response. Missing field: {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
