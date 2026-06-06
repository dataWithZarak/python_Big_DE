import requests
import json

api_key = "9f5d51880243265e4b4c0b30fca8a9e6"
city = "Peshawar"

url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={city}&appid={api_key}&units=metric"
)

response = requests.get(url)
print(response)

data = response.json()
print(data)


city_name = data["name"]
temperature = data["main"]["temp"]
description = data["weather"][0]["description"]

print (city_name, temperature, description)


with open("weather.json", "w") as file:
    json.dump(data, file, indent=4)


def fetch_weather(city: str, api_key: str) -> dict:
    """
    Fetch current weather for a city from OpenWeatherMap.
    Returns the parsed JSON dict on success.
    Raises a descriptive RuntimeError on any failure.
    """
    url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={city}&amp;appid={api_key}&amp;units=metric"
    )
    try:
        response = requests.get(url, timeout=10) # ← always set a timeout
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Network error: could not reach the API.")
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out after 10 seconds.")
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Unexpected request error: {exc}")
# Check HTTP status code
    if response.status_code == 401:
        raise RuntimeError("Invalid API key. Check your credentials.")
    if response.status_code == 404:
        raise RuntimeError(f"City'{city}' not found. Check spelling.")
    if response.status_code != 200:
        raise RuntimeError(f"API returned status {response.status_code}.")
    # Parse JSON safely
    try:
        data = response.json()
    except ValueError:
        raise RuntimeError("API response is not valid JSON.")
    return data



def extract_fields(data: dict) -> dict:

    """Pull only the fields we need from the raw API response.
    Uses .get() to avoid KeyError if a field is missing.
    """
    main = data.get('main', {})
    weather = data.get('weather', [{}])
    return {
        'city': data.get('name', 'Unknown'),
        'temperature': main.get('temp'),
        'humidity': main.get('humidity'),
        'description': weather[0].get('description', 'N/A'),
        'wind_speed': data.get('wind', {}).get('speed'),
    }

def save_locally(data: dict, filename: str) -> None:
    """Save dict as a formatted JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f'Saved locally → {filename}')
    except OSError as exc:
        raise RuntimeError(f'Could not write file {filename}: {exc}')