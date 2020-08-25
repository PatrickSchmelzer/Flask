import datetime
import requests
#import dateutil.parser
import pprint
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#import numpy as np

INHABITANTS_ITALY_FACTOR = 100000 / 60260229
INHABITANTS_SWITZERLAND_FACTOR = 100000 / 8603900
INHABITANTS_GERMANY_FACTOR = 100000 / 83166711
INHABITANTS_SPAIN_FACTOR = 100000 / 47100396
INHABITANTS_FRANCE_FACTOR = 100000 / 66993000

def getInhabitants():
    inhabitants = {}
    inhabitants["Italy"] = 60260229
    inhabitants["Switzerland"] = 8603900
    inhabitants["Germany"] = 83166711
    inhabitants["Spain"] = 47100396
    inhabitants["France"] = 66993000
    inhabitants["UK"] = 66435550
    inhabitants["USA"] = 328000000

    return inhabitants

def getCovidData():
    summaryUrl = 'https://api.covid19api.com/summary'
    entries = requests.get(summaryUrl).json()
    data = {}
    dataWorld = entries["Global"]
    data["World"] = {"NewConfirmed": dataWorld["NewConfirmed"], "NewDeaths": dataWorld["NewDeaths"], "NewRecovered": dataWorld["NewRecovered"], 
                  "TotalConfirmed": dataWorld["TotalConfirmed"], "TotalDeaths": dataWorld["TotalDeaths"], "TotalRecovered": dataWorld["TotalRecovered"]}
    
    entryCountries = entries["Countries"]
    for entry in entryCountries:
        if entry['Country'] == "United Kingdom":
            data["UK"] = {"NewConfirmed": entry["NewConfirmed"], "NewDeaths": entry["NewDeaths"], "NewRecovered": entry["NewRecovered"], 
                  "TotalConfirmed": entry["TotalConfirmed"], "TotalDeaths": entry["TotalDeaths"], "TotalRecovered": entry["TotalRecovered"]}
        elif entry['Country'] == "United States of America":
            data["USA"] = {"NewConfirmed": entry["NewConfirmed"], "NewDeaths": entry["NewDeaths"], "NewRecovered": entry["NewRecovered"], 
                  "TotalConfirmed": entry["TotalConfirmed"], "TotalDeaths": entry["TotalDeaths"], "TotalRecovered": entry["TotalRecovered"]}
        else:
            data[entry["Country"]] = {"NewConfirmed": entry["NewConfirmed"], "NewDeaths": entry["NewDeaths"], "NewRecovered": entry["NewRecovered"], 
                  "TotalConfirmed": entry["TotalConfirmed"], "TotalDeaths": entry["TotalDeaths"], "TotalRecovered": entry["TotalRecovered"]}
    
    #msg = "New Covid Data for today\n\n"
    #msg += "New Cases World: " + str(data["World"]["NewConfirmed"]) + "\n"
    #msg += "New Cases Italy: " + str(data["Italy"]["NewConfirmed"]) + ", Cases/100'000: " + str(round(data["Italy"]["NewConfirmed"] * INHABITANTS_ITALY_FACTOR,2)) + "\n"
    #msg += "New Cases Switzerland: " + str(data["Switzerland"]["NewConfirmed"]) + ", Cases/100'000: "+ str(round(data["Switzerland"]["NewConfirmed"] * INHABITANTS_SWITZERLAND_FACTOR,2)) + "\n"
    #msg += "New Cases Germany: " + str(data["Germany"]["NewConfirmed"]) + ", Cases/100'000: "+ str(round(data["Germany"]["NewConfirmed"] * INHABITANTS_GERMANY_FACTOR,2)) + "\n"
    #msg += "New Cases Spain: " + str(data["Spain"]["NewConfirmed"]) + ", Cases/100'000: "+ str(round(data["Spain"]["NewConfirmed"] * INHABITANTS_SPAIN_FACTOR,2)) + "\n"
    #msg += "New Cases France: " + str(data["France"]["NewConfirmed"]) + ", Cases/100'000: "+ str(round(data["France"]["NewConfirmed"] * INHABITANTS_FRANCE_FACTOR,2)) + "\n"
    return data