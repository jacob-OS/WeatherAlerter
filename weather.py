import re
import requests

from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim


def locate(zipcode, country="United States"):
    geolocator = Nominatim(user_agent="Geolocation")
    lc = geolocator.geocode(f"{zipcode}, {country}", timeout=1000)  # location
    return lc


def currentTemperature(zipcode, fahrenheit=bool()):  # retrieves the current temperature
    lat = locate(zipcode=zipcode).latitude   # latitude
    lon = locate(zipcode=zipcode).longitude  # longitude

    url = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}#XtpdeOfhXIX"
    bsoup = BeautifulSoup(requests.get(url).content, features="html.parser")

    items = bsoup.find("div", id="current_conditions-summary")

    if fahrenheit is True:  # if set to fahrenheit
        temperature = items.find(class_="myforecast-current-lrg").get_text()

    else:                   # if not set to fahrenheit
        temperature = items.find(class_="myforecast-current-sm").get_text()

    return temperature


def futureForecast(zipcode):  # retrieves data for each hour of the next 48 hours
    lat = locate(zipcode=zipcode).latitude   # latitude
    lon = locate(zipcode=zipcode).longitude  # longitude

    url = f"https://forecast.weather.gov/MapClick.php?lat={round(lat, 4)}&lon={round(lon, 4)}&FcstType=digitalDWML"
    bsoup = BeautifulSoup(requests.get(url).content, features="xml")

    data = {
        "times": bsoup.find("time-layout").find_all("start-valid-time"),          # timestamps
        "tmper": bsoup.find("temperature", type="hourly").find_all("value"),      # temperature (F)
        "dewpt": bsoup.find("temperature", type="dew point").find_all("value"),   # dewpoint (F)
        "htidx": bsoup.find("temperature", type="heat index").find_all("value"),  # heat index (F)
        "wdspd": bsoup.find("wind-speed").find_all("value"),                      # wind speed (MPH)
        "wddir": bsoup.find("direction").find_all("value"),                       # wind direction (degrees)
        "skycv": bsoup.find("cloud-amount").find_all("value"),                    # sky cover (%)
        "prcpt": bsoup.find("probability-of-precipitation").find_all("value"),    # precipitation potential (%)
        "humid": bsoup.find("humidity").find_all("value")                         # relative humidity (%)
    }

    for i in range(len(data["times"])):
        for slash in ['', '/']:
            data["times"][i] = re.sub(f"<{slash}start-valid-time>", '', str(data["times"][i]))

        dateInfo = {
            "y": '',  # year
            "m": '',  # month
            "d": '',  # day
            "h": ''   # hour
        }

        for j in range(0, 4):
            dateInfo["y"] += str(data["times"][i][j])  # enters year
        for j in range(5, 7):
            dateInfo["m"] += str(data["times"][i][j])  # enters month
        for j in range(8, 10):
            dateInfo["d"] += str(data["times"][i][j])  # enters day
        for j in range(11, 13):
            dateInfo["h"] += str(data["times"][i][j])  # enters hour

        data["times"][i] = dateInfo

    for element in ["tmper", "dewpt", "htidx", "wdspd", "wddir", "skycv", "prcpt", "humid"]:
        for i in range(len(data[element])):
            for slash in ['', '/']:
                data[element][i] = re.sub(f"<{slash}value>", '', str(data[element][i]))

    return data


def futureMaxMin(data, obj=str()):
    mx = int(data[obj][0])  # maximum (initial value is the first value)
    mn = mx                 # minimum (initial value is the first value)

    tmx = []  # times at which the maximums occurred
    tmn = []  # times at which the maximums occurred

    for i in range(len(data[obj])):
        value = int(data[obj][i])  # current value
        stamp = data["times"][i]   # timestamp

        if mx == value:
            tmx.append(stamp)
        elif mx < value:
            tmx = [stamp]
            mx = value

        if mn == value:
            tmn.append(stamp)
        elif mn > value:
            tmn = [stamp]
            mn = value

    return {
        "max": {
            "value": mx,  # value of the max
            "times": tmx  # timestamp(s) of the max
        },
        "min": {
            "value": mn,  # value of the min
            "times": tmn  # timestamp(s) of the min
        }
    }
