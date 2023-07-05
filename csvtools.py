import csv
import pandas as pd
import re

from ast import literal_eval as le


def addUser(name=None, email=None, phone=None, zipcode=None, country=None):
    info = {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "ZipCode": zipcode,
        "Country": country,
        "Alerts": {
            "tmper": {"abv": None, "blo": None},
            "dewpt": {"abv": None, "blo": None},
            "htidx": {"abv": None, "blo": None},
            "wdspd": {"abv": None, "blo": None},
            "wddir": {"abv": None, "blo": None},
            "skycv": {"abv": None, "blo": None},
            "prcpt": {"abv": None, "blo": None},
            "humid": {"abv": None, "blo": None}},
        "LastAlerts": {
            "tmper": {"abv": None, "blo": None},
            "dewpt": {"abv": None, "blo": None},
            "htidx": {"abv": None, "blo": None},
            "wdspd": {"abv": None, "blo": None},
            "wddir": {"abv": None, "blo": None},
            "skycv": {"abv": None, "blo": None},
            "prcpt": {"abv": None, "blo": None},
            "humid": {"abv": None, "blo": None}}
    }

    with open("users.csv", "a") as f:
        dictObj = csv.DictWriter(f, fieldnames=[
            "Name", "Email", "Phone", "ZipCode", "Country", "Alerts", "LastAlerts"
        ])
        dictObj.writerow(info)


def remUser(email=None, phone=None):

    df = pd.read_csv("users.csv", sep=",")

    if email:
        df = df.drop(df[df.Email == email].index)
    elif phone:
        df = df.drop(df[df.Phone == phone].index)

    df.to_csv("users.csv", index=False)


def addAlert(email=None, phone=None, alert=None, above=True, value=None):

    df = pd.read_csv("users.csv", sep=",")

    if alert and (email or phone):

        if email:
            a = "Email"
            b = email
        else:
            a = "Phone"
            b = phone

        ALERT = le(df[df[a] == b]["Alerts"][df.index[df[a] == b].tolist()[0]])

        alerts = {
            "tmper": {"abv": ALERT["tmper"]["abv"], "blo": ALERT["tmper"]["blo"]},
            "dewpt": {"abv": ALERT["dewpt"]["abv"], "blo": ALERT["dewpt"]["blo"]},
            "htidx": {"abv": ALERT["htidx"]["abv"], "blo": ALERT["htidx"]["blo"]},
            "wdspd": {"abv": ALERT["wdspd"]["abv"], "blo": ALERT["wdspd"]["blo"]},
            "wddir": {"abv": ALERT["wddir"]["abv"], "blo": ALERT["wddir"]["blo"]},
            "skycv": {"abv": ALERT["skycv"]["abv"], "blo": ALERT["skycv"]["blo"]},
            "prcpt": {"abv": ALERT["prcpt"]["abv"], "blo": ALERT["prcpt"]["blo"]},
            "humid": {"abv": ALERT["humid"]["abv"], "blo": ALERT["humid"]["blo"]}
        },

        if above is True:
            alerts[0][alert]["abv"] = value
        else:
            alerts[0][alert]["blo"] = value

        df.loc[df[a] == b, "Alerts"] = alerts

    df.to_csv("users.csv", index=False)


def remAlert(email=None, phone=None, alert=None, above=True):

    df = pd.read_csv("users.csv", sep=",")

    if alert and (email or phone):

        if email:
            a = "Email"
            b = email
        else:
            a = "Phone"
            b = phone

        ALERT = le(df[df[a] == b]["Alerts"][df.index[df[a] == b].tolist()[0]])

        alerts = {
            "tmper": {"abv": ALERT["tmper"]["abv"], "blo": ALERT["tmper"]["blo"]},
            "dewpt": {"abv": ALERT["dewpt"]["abv"], "blo": ALERT["dewpt"]["blo"]},
            "htidx": {"abv": ALERT["htidx"]["abv"], "blo": ALERT["htidx"]["blo"]},
            "wdspd": {"abv": ALERT["wdspd"]["abv"], "blo": ALERT["wdspd"]["blo"]},
            "wddir": {"abv": ALERT["wddir"]["abv"], "blo": ALERT["wddir"]["blo"]},
            "skycv": {"abv": ALERT["skycv"]["abv"], "blo": ALERT["skycv"]["blo"]},
            "prcpt": {"abv": ALERT["prcpt"]["abv"], "blo": ALERT["prcpt"]["blo"]},
            "humid": {"abv": ALERT["humid"]["abv"], "blo": ALERT["humid"]["blo"]}
        },

        if above is True:
            alerts[0][alert]["abv"] = None
        else:
            alerts[0][alert]["blo"] = None

        df.loc[df[a] == b, "Alerts"] = alerts

    df.to_csv("users.csv", index=False)


addAlert(email="J@gmail.com", alert="dewpt", above=False, value=32)
