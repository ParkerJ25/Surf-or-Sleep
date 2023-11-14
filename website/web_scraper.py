from bs4 import BeautifulSoup
import requests
import math

SURF_FORECAST_URL = "https://www.surf-forecast.com/breaks/Huntington-Pier/forecasts/latest/six_day"
SURF_CAPTAIN_URL = "https://surfcaptain.com/forecast/huntington-beach-california"

def send_request_and_parse(url, class_name):
    result = requests.get(url)
    result.raise_for_status()
    doc = BeautifulSoup(result.text, "html.parser")
    data = doc.find_all(class_=class_name)
    return data

def scrape_surf_forecast_water_temp():
    water_temp_data = send_request_and_parse(SURF_FORECAST_URL, "temp")
    water_temp_celsius = float(water_temp_data[0].get_text(strip=True))
    water_temp_fahrenheit = (water_temp_celsius * 1.8) + 32
    temp = math.ceil(water_temp_fahrenheit)
    return temp

def scrape_surf_forecast_wave_height():
    wave_height_data = send_request_and_parse(SURF_FORECAST_URL, "swell-icon__val")
    am_wave_height = float(wave_height_data[0].get_text(strip=True)) * 3.3
    pm_wave_height = float(wave_height_data[1].get_text(strip=True)) * 3.3
    return math.ceil(am_wave_height), math.ceil(pm_wave_height)

def scrape_surf_forecast_wind_mph():
    wind_mph_data = send_request_and_parse(SURF_FORECAST_URL, "wind-icon__val")
    am_wind_mph = int(wind_mph_data[0].get_text(strip=True))
    pm_wind_mph = int(wind_mph_data[1].get_text(strip=True))
    am_wind_mph = am_wind_mph - 5 if am_wind_mph > 0 else am_wind_mph
    pm_wind_mph = pm_wind_mph - 5 if pm_wind_mph > 0 else pm_wind_mph
    return am_wind_mph, pm_wind_mph

def scrape_surf_captain_water_temp():
    water_temp_data = send_request_and_parse(SURF_CAPTAIN_URL, "current-data-desc")
    water_temp_number = ''.join(filter(str.isdigit, water_temp_data[3].get_text(strip=True)))[:2]
    return water_temp_number

def scrape_surf_captain_wave_height():
    wave_height_data = send_request_and_parse(SURF_CAPTAIN_URL, "hourly-surf clean")
    am_wave_height = wave_height_data[0].get_text(strip=True)
    pm_wave_height = wave_height_data[1].get_text(strip=True)
    pm_wave_height = ' '.join(filter(str.isdigit, pm_wave_height))
    am_wave_height = ' '.join(filter(str.isdigit, am_wave_height))
    am_wave_height = [int(height) for height in am_wave_height]
    am_wave_height = sum(am_wave_height) / len(am_wave_height)
    pm_wave_height = [int(height) for height in pm_wave_height]
    pm_wave_height = sum(pm_wave_height) / len(pm_wave_height)
    return am_wave_height, pm_wave_height

def scrape_surf_captain_wind_mph():
    wind_mph_data = send_request_and_parse(SURF_CAPTAIN_URL, "hourly-wind-spd")
    
    # Extract numeric part and convert to integer, defaulting to 0 if not present
    am_wind_speed = int(''.join(filter(str.isdigit, wind_mph_data[0].get_text(strip=True)))) or 0
    pm_wind_speed = int(''.join(filter(str.isdigit, wind_mph_data[1].get_text(strip=True)))) or 0
    
    return am_wind_speed, pm_wind_speed


def average_wind(am_surf_captain, pm_surf_captain, am_surf_forecast, pm_surf_forecast):
    am_average = math.ceil((am_surf_captain + am_surf_forecast) / 2)
    pm_average = math.ceil((pm_surf_captain + pm_surf_forecast) / 2)
    print("Average AM Winds: ", am_average, "MPH")
    print("Average PM Winds: ", pm_average, "MPH")
    print("")
    return am_average, pm_average

def average_wave_height(am_surf_forecast, pm_surf_forecast, am_surf_captain, pm_surf_captain):
    am_average = math.ceil((am_surf_captain + am_surf_forecast) / 2)
    pm_average = math.ceil((pm_surf_captain + pm_surf_forecast) / 2)
    print("Average AM Wave Height: ", am_average)
    print("Average PM Wave Height: ", pm_average)
    print("")
    return am_average, pm_average

def average_water_temp(surf_forecast, surf_captain):
    average = math.ceil((float(surf_captain) + float(surf_forecast)) / 2)
    print("Average Water Temp: ", average)
    return average

def get_scraped_data():
    # Wind Conditions #
    am_wind_speed_surf_captain, pm_wind_speed_surf_captain = scrape_surf_captain_wind_mph()
    am_wind_speed_surf_forecast, pm_wind_speed_surf_forecast = scrape_surf_forecast_wind_mph()
    am_wind, pm_wind = average_wind(am_wind_speed_surf_captain, pm_wind_speed_surf_captain, am_wind_speed_surf_forecast, pm_wind_speed_surf_forecast)

    # Wave Height Conditions #
    am_wave_height_surf_forecast, pm_wave_height_surf_forecast = scrape_surf_forecast_wave_height()
    am_wave_height_surf_captain, pm_wave_height_surf_captain = scrape_surf_captain_wave_height()
    am_wave, pm_wave = average_wave_height(am_wave_height_surf_forecast, pm_wave_height_surf_forecast, am_wave_height_surf_captain, pm_wave_height_surf_captain)

    # Water Temp Conditions
    water_temp_surf_forecast = scrape_surf_forecast_water_temp()
    water_temp_surf_captain = scrape_surf_captain_water_temp()
    water_temp = average_water_temp(water_temp_surf_forecast, water_temp_surf_captain)

    scraped_data = {
        "am_wind": am_wind,
        "pm_wind": pm_wind,
        "am_wave": am_wave,
        "pm_wave": pm_wave,
        "water_temp": water_temp,
    }

    return scraped_data

if __name__ == "__main__":
   scraped_data = get_scraped_data()
   print(scraped_data)
