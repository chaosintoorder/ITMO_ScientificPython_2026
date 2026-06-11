# To use this API you have to install openmeteo_requests library'
import openmeteo_requests
from datetime import datetime


openmeteo = openmeteo_requests.Client()
url = "https://api.open-meteo.com/v1/forecast"
params = {
"latitude": 59.9386, # for St.Petersburg
"longitude": 30.3141, # for St.Petersburg
"current": ["temperature_2m", "apparent_temperature", "rain", "wind_speed_10m"],
"wind_speed_unit": "ms",
"timezone": "Europe/Moscow"
}

response = openmeteo.weather_api(url, params=params)[0]

# The order of variables needs to be the same as requested in params->current!
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_apparent_temperature = current.Variables(1).Value()
current_rain = current.Variables(2).Value()
current_wind_speed_10m = current.Variables(3).Value()

print(f"Current time: {datetime.fromtimestamp(current.Time()+response.UtcOffsetSeconds())} {response.TimezoneAbbreviation().decode()}")
print(f"Current temperature: {round(current_temperature_2m, 0)} C")
print(f"Current apparent_temperature: {round(current_apparent_temperature, 0)} C")
print(f"Current rain: {current_rain} mm")
print(f"Current wind_speed: {round(current_wind_speed_10m, 1)} m/s")