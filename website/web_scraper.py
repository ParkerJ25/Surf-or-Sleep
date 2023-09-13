from bs4 import BeautifulSoup
import requests
import math
#------------------------------ Scraping for Surf-Forecast.com---------------------------------------#
def scrape_surf_forecast_water_temp():
    print("--------------- Data for Surf-Forecast.com -----------------")
    # Define the URL for the website that has conditions for North Orange County beaches
    url = "https://www.surf-forecast.com/breaks/Huntington-Pier/forecasts/latest/six_day"

    # Send a GET request to the specified URL and retrieve the text content
    result = requests.get(url).text

    # Parse the HTML content of the response using BeautifulSoup
    doc = BeautifulSoup(result, "html.parser")

    surf_forecast_water_temp = doc.find_all(class_="temp")
    water_temp = surf_forecast_water_temp[0].get_text(strip=True)
    water_temp_celsius = float(water_temp)
    water_temp_farenheight = (water_temp_celsius) * 1.8 + 32
    temp = math.ceil(water_temp_farenheight)
    print("Water temp: ", temp)
    return temp

#scrape_surf_forecast_water_temp()

def scrape_surf_forecast_wave_height():
    # Define the URL for the website that has conditions for North Orange County beaches
    url = "https://www.surf-forecast.com/breaks/Huntington-Pier/forecasts/latest/six_day"

    # Send a GET request to the specified URL and retrieve the text content
    result = requests.get(url).text

    # Parse the HTML content of the response using BeautifulSoup
    doc = BeautifulSoup(result, "html.parser")

    surf_forecast_wave_height = doc.find_all(class_="swell-icon__val")
    am_wave_height = surf_forecast_wave_height[0].get_text(strip=True)
    am_wave_height = float(am_wave_height)
    am_wave_height *= 3.3
    am_wave_height = math.ceil(am_wave_height)
    pm_wave_height = surf_forecast_wave_height[1].get_text(strip=True)
    pm_wave_height = float(pm_wave_height)
    pm_wave_height *= 3.3
    pm_wave_height = math.ceil(pm_wave_height)
    print(f"AM Wave Height: {am_wave_height}")
    print(f"PM Wave Height: {pm_wave_height}")
    return am_wave_height, pm_wave_height

#scrape_surf_forecast_wave_height()

def scrape_surf_forecast_wind_mph():
    url = "https://www.surf-forecast.com/breaks/Huntington-Pier/forecasts/latest/six_day"

    # Send a GET request to the specified URL and retrieve the text content
    result = requests.get(url).text

    # Parse the HTML content of the response using BeautifulSoup
    doc = BeautifulSoup(result, "html.parser")
    surf_forecast_wind_mph = doc.find_all(class_="wind-icon__val")
    am_wind_mph = surf_forecast_wind_mph[0].get_text(strip=True)
    pm_wind_mph = surf_forecast_wind_mph[1].get_text(strip=True)
    am_wind_mph = int(am_wind_mph)
    pm_wind_mph = int(pm_wind_mph)
    am_wind_mph -= 5
    pm_wind_mph -= 5
    print(f"AM Wind (MPH): {am_wind_mph}")
    print(f"PM Wind (MPH): {pm_wind_mph}")
    print("")
    return am_wind_mph, pm_wind_mph
    
#scrape_surf_forecast_wind_mph()
#------------------------------ Scraping for SwellInfo.com-----------------------------------------#

def scrape_swell_info_water_temp():

    print("--------------- Data for SwellInfo.com -----------------")
    # Define the URL for the website that has conditions for North Orange County beaches
    url = "https://www.swellinfo.com/surf-forecast/orange-county-california-north"

    # Send a GET request to the specified URL and retrieve the text content
    result = requests.get(url).text

    # Parse the HTML content of the response using BeautifulSoup
    doc = BeautifulSoup(result, "html.parser")

    swell_info_water_temp = doc.find_all(class_="wx-icon-water-data")
    water_temp = swell_info_water_temp[0].get_text(strip=True)
    water_temp_number = ''.join(filter(str.isdigit, water_temp))
    print("Water Temp: ", water_temp_number)
    return water_temp_number

#scrape_swell_info_water_temp()


def scrape_swell_info_wave_heights():
    # Define the URL for the website that has conditions for North Orange County beaches
    url = "https://www.swellinfo.com/surf-forecast/orange-county-california-north"

    # Send a GET request to the specified URL and retrieve the text content
    result = requests.get(url).text

    # Parse the HTML content of the response using BeautifulSoup
    doc = BeautifulSoup(result, "html.parser")

    # Find elements that contain surf condition data (wave height)
    swell_info_wave_height = doc.find_all(class_="fcst-day-wvht")
    
    # Extract wave height for "am" and "pm" and remove extra whitespaces
    am_wave_height = swell_info_wave_height[0].get_text(strip=True)
    pm_wave_height = swell_info_wave_height[1].get_text(strip=True)

    am_wave_height = am_wave_height.split('-')[0] if '-' in am_wave_height else am_wave_height
    pm_wave_height = pm_wave_height.split('-')[0] if '-' in pm_wave_height else pm_wave_height
    
    # Replace 'flat' with '0' if present
    am_wave_height = '0' if am_wave_height.lower() == 'flat' else am_wave_height
    pm_wave_height = '0' if pm_wave_height.lower() == 'flat' else pm_wave_height
    
    # Print the wave heights
    print(f"AM Wave Height: {am_wave_height}")
    print(f"PM Wave Height: {pm_wave_height}")
    return am_wave_height, pm_wave_height

# Call the function to scrape and print wave heights
#scrape_swell_info_wave_heights()

def scrape_swell_info_wind_mph():
    # Define the URL for the website that has conditions for North Orange County beaches
    url = "https://www.swellinfo.com/surf-forecast/orange-county-california-north"

    # Send a GET request to the specified URL and retrieve the text content
    result = requests.get(url).text

    # Parse the HTML content of the response using BeautifulSoup
    doc = BeautifulSoup(result, "html.parser")

    # Find elements that contain surf condition data (wind speed)
    swell_info_wind_mph = doc.find_all(class_="fcst-day-hourly-wind-mph")

    # Initialize a list to store the extracted wind speeds
    wind_speeds = []

    # Define the times you want to associate with the wind speeds
    times = ["AM Wind","PM Wind"]

    # Iterate through the elements and extract the numeric part from the parent <div> element
    for i, mph in enumerate(swell_info_wind_mph):
        # Get the parent <div> element and extract the text
        parent_div = mph.parent
        text = parent_div.get_text(strip=True)

        # Extract the numeric part (remove non-numeric characters)
        numeric_part = ''.join(filter(str.isdigit, text))

        # Append the numeric part along with the corresponding time
        if i < len(times):
            wind_speeds.append(f"{times[i]}: {numeric_part} mph")

    # Print the list of wind speeds
    print(wind_speeds)
    print("")
    return wind_speeds

# Call the function to perform the web scraping and display wind speeds
#scrape_swell_info_wind_mph()

#---------------------------------- Scraping for SurfCaptain-----------------------------------------#

def scrape_surf_captain_water_temp():

    print("--------------- Data for SurfCaptain.com -----------------")

    url = "https://surfcaptain.com/forecast/huntington-beach-california"
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")
    surf_captain_water_temp = doc.find_all(class_="current-data-desc")
    water_temp = surf_captain_water_temp[3].get_text(strip=True)
    water_temp_number = ''.join(filter(str.isdigit, water_temp))
    water_temp_number = water_temp_number[:2]
    print("Water Temp:", water_temp_number)
    return water_temp_number

#scrape_surf_captain_water_temp()

def scrape_surf_captain_wave_height():
    url = "https://surfcaptain.com/forecast/huntington-beach-california"
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")
    surf_captain_wave_height_am = doc.find_all(class_="hourly-surf clean")
    am_wave_height = surf_captain_wave_height_am[0].get_text(strip=True)
    pm_wave_height = surf_captain_wave_height_am[1].get_text(strip=True)
    pm_wave_height = ' '.join(filter(str.isdigit, pm_wave_height))
    am_wave_height = ' '.join(filter(str.isdigit, am_wave_height))      # Might have to fix the pm_wave_height_later if there are too many inconsistencies 
    pm_wave_height = pm_wave_height.split()
    am_wave_height = am_wave_height.split()
    am_wave_height = [int(height) for height in am_wave_height]
    am_wave_height = sum(am_wave_height) / len(am_wave_height)
    pm_wave_height = [int(height) for height in pm_wave_height]
    pm_wave_height = sum(pm_wave_height) / len(pm_wave_height)
    print(f"AM Wave Height: {am_wave_height}")
    print(f"PM Wave Height: {pm_wave_height}")
    return am_wave_height, pm_wave_height

#scrape_surf_captain_wave_height()

def scrape_surf_captain_wind_mph():
    url = "https://surfcaptain.com/forecast/huntington-beach-california"
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")
    am_wind_speed = None
    pm_wind_speed = None

    surf_captain_wind_mph = doc.find_all(class_="hourly-wind-spd")
    for i, mph in enumerate(surf_captain_wind_mph):
        text = mph.get_text(strip=True)
        numeric_part = ''.join(filter(str.isdigit, text))
        if i == 0:
            am_wind_speed = int(numeric_part)
        elif i == 1:
            pm_wind_speed = int(numeric_part)
    return am_wind_speed, pm_wind_speed

#scrape_surf_captain_wind_mph()


def average_wind(am_surf_captain, pm_surf_captain, am_swell_info, pm_swell_info, am_surf_forecast, pm_surf_forecast):
    # AM Wind Average Calculation
    print("------------------- Average Conditions----------------------")
    numeric_part = am_swell_info.replace(' mph', '').split(': ')[-1]
    am_swell_info = float(numeric_part)
    am_surf_captain = float(am_surf_captain)
    am_surf_forecast = float(am_surf_forecast)
    am_average = math.ceil((am_surf_captain + am_swell_info + am_surf_forecast) / 3)
    print("Average AM Winds: ", am_average, "MPH")
    # PM Wind Average Calculation
    numeric_part = pm_swell_info.replace(' mph', '').split(': ')[-1]
    pm_swell_info = float(numeric_part)
    pm_surf_captain = float(pm_surf_captain)
    pm_surf_forecast = float(pm_surf_forecast)
    pm_average = math.ceil((pm_swell_info + pm_surf_captain + pm_surf_forecast) / 3)
    print("Average PM Winds: ", pm_average, "MPH")
    print("")
    

def average_wave_height(am_swell_info, pm_swell_info, am_surf_forecast, pm_surf_forecast, am_surf_captain, pm_surf_captain):
    am_swell_info = float(am_swell_info)
    am_surf_captain = float(am_surf_captain)
    am_surf_forecast = float(am_surf_forecast)
    am_average = math.ceil((am_swell_info + am_surf_captain + am_surf_forecast) / 3)
    print("Average AM Wave Height: ", am_average)
    pm_swell_info = float(pm_swell_info)
    pm_surf_captain = float(pm_surf_captain)
    pm_surf_forecast = float(pm_surf_forecast)
    pm_average = math.ceil((pm_swell_info + pm_surf_captain + pm_surf_forecast) / 3)
    print("Average AM Wave Height: ", pm_average)


def average_water_temp(swell_info, surf_forecast, surf_captain):
    swell_info = float(swell_info)
    surf_forecast = float(surf_forecast)
    surf_captain = float(surf_captain)
    average = math.ceil((swell_info + surf_captain + surf_forecast) / 3)
    print("Average Water Temp: ", average)
    print("")

def main():
    # Wind Conditions #
    wind_speed_surf_captain = scrape_surf_captain_wind_mph()
    am_wind_speed_surf_captain, pm_wind_speed_surf_captain = wind_speed_surf_captain
    wind_speed_swell_info = scrape_swell_info_wind_mph()
    am_wind_speed_swell_info, pm_wind_speed_swell_info = wind_speed_swell_info
    wind_speed_surf_forecast = scrape_surf_forecast_wind_mph()
    am_wind_speed_surf_forecast, pm_wind_speed_surf_forecast = wind_speed_surf_forecast
    average_wind(am_wind_speed_surf_captain, pm_wind_speed_surf_captain, am_wind_speed_swell_info, pm_wind_speed_swell_info, am_wind_speed_surf_forecast, pm_wind_speed_surf_forecast)
    # Wave Height Conditions #
    am_wave_height_swell_info, pm_wave_height_swell_info = scrape_swell_info_wave_heights()
    am_wave_height_surf_forecast, pm_wave_height_surf_forecast = scrape_surf_forecast_wave_height()
    am_wave_height_surf_captain, pm_wave_height_surf_captain = scrape_surf_captain_wave_height()
    average_wave_height(am_wave_height_swell_info, pm_wave_height_swell_info, am_wave_height_surf_forecast, pm_wave_height_surf_forecast, am_wave_height_surf_captain, pm_wave_height_surf_captain)
    # Water Temp Conditions
    water_temp_swell_info = scrape_swell_info_water_temp()
    water_temp_surf_forecast = scrape_surf_forecast_water_temp()
    water_temp_surf_captain = scrape_surf_captain_water_temp()
    average_water_temp(water_temp_swell_info, water_temp_surf_forecast, water_temp_surf_captain)

if __name__ == "__main__":
    main()




