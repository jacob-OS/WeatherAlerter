import pandas as pd
import weather

from ast import literal_eval as le
from datetime import datetime as dt


def formData(email=None, phone=None):
    data = []

    df = pd.read_csv("users.csv", sep=",")

    if email:
        a = "Email"
        b = email
    else:
        a = "Phone"
        b = phone

    ALERT = le(df[df[a] == b]["Alerts"][df.index[df[a] == b].tolist()[0]])

    forecast = weather.futureForecast(df[df[a] == b]["ZipCode"].tolist()[0])

    for alert in ["tmper", "dewpt", "htidx", "wdspd", "wddir", "skycv", "prcpt", "humid"]:

        if ALERT[alert]["abv"]:
            abv = int(ALERT[alert]["abv"])

            for i in range(len(forecast["times"])):

                try:
                    if int(forecast[alert][i]) > abv:
                        data.append([{
                            "t": forecast["times"][i],
                            "a": alert,
                            "abv/blo": "abv",
                            "v": int(ALERT[alert]["abv"])
                        }])
                except ValueError:
                    pass

        if ALERT[alert]["blo"]:
            blo = int(ALERT[alert]["blo"])

            for i in range(len(forecast["times"])):

                try:
                    if int(forecast[alert][i]) < blo:
                        data.append([{
                            "t": forecast["times"][i],
                            "a": alert,
                            "abv/blo": "blo",
                            "v": int(ALERT[alert]["blo"])
                        }])
                except ValueError:
                    pass

    return data


def textualize(data):
    TRANSLATIONS = {
        "tmper": "temperature",
        "dewpt": "dew point",
        "htidx": "heat index",
        "wdspd": "wind speed",
        "wddir": "wind direction",
        "skycv": "sky cover",
        "prcpt": "precipitation",
        "humid": "humidity"
    }

    lines = []

    date = ""
    for alert in data:

        hour = dt.strptime(f"{int(alert[0]['t']['h'])}:00", "%H:%M").strftime("%I:%M %p")

        alertDate = f"{alert[0]['t']['m']}/{alert[0]['t']['d']}/{alert[0]['t']['y']}"

        if alert[0]["abv/blo"] == "abv":
            abv_blo = "rise above"
        else:
            abv_blo = "fall below"

        if alertDate != date:
            lines.append(f"{alertDate}:")
            date = alertDate

        lines.append(f"at {hour} the {TRANSLATIONS[alert[0]['a']]} will {abv_blo} {alert[0]['v']}")

    return lines

