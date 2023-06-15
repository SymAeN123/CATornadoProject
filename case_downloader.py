import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz
from downloader import download_radar_data
import sys
root = __file__.removesuffix("case_downloader.py")
os.chdir(root)

target_csv = "Ameya_storm_data_search_results.csv"

valid_radars = {"KDAX", "KBBX", "KHNX", "KEYX", "KNKX", "KSOX", "KESX", "KRGX", "KYUX", "KVTX", "KVBX", "KMUX", "KMAX", "KBHX"}

events = pd.read_csv(".\\spreadsheets\\" + target_csv)

dl_cases = list(map(lambda x: int(x), os.listdir(root+"cases\\")))

all_cases = list(events["EVENT_ID"])
remaining_cases = list(filter(lambda x: x not in dl_cases, all_cases))

#helper functions
def mapsLink(lat, lon):
    uri = "https://www.google.com/maps/search/?api=1&query="+str(lat)+"%2C"+str(lon)+""
    parameters = ""
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, uri)


#Choose case to download
print("Choose one of the following cases to download:")
print(remaining_cases)
while True:
    try:
        choice = int(input("Choice: "))
    except ValueError:
        print("Input cannot be converted to int")
        continue
    if choice not in remaining_cases:
        print("Invalid Choice")
    else:
        break

#Get data from main CSV
event = events[events["EVENT_ID"] == choice]
date = event["BEGIN_DATE"].values[0].split("/")
latitude = event["BEGIN_LAT"].values[0]
longitude = event["BEGIN_LON"].values[0]
time = str(event["BEGIN_TIME"].values[0])
if len(time) == 1:
    time = "00:0"+time
elif len(time) == 2:
    time = "00:"+time
elif len(time) == 3:
    time = "0"+time[:1]+':'+time[1:]
else:
    time = time[:2]+':'+time[2:]
time = time.split(":")
local_timezone = pytz.timezone("America/Los_Angeles")
local_time = local_timezone.localize(datetime(int(date[2]), int(date[0]), int(date[1]), int(time[0]), int(time[1])))
print("Local time:")
print(local_time)
utc = local_time.astimezone(pytz.utc)
print("UTC Time")
print(utc)
utc = utc.replace(tzinfo=None)
begin_time = utc-timedelta(hours=2)
end_time = utc+timedelta(hours=2)

#Select radar sites to download
print("The coordinates are:", str(latitude)+","+str(longitude))
print(mapsLink(latitude, longitude))
print("Valid Radars Are:", valid_radars)
while True:
    sites = input("Select Radar Sites to Download (space separated): ").split(" ")
    if not set(sites).issubset(valid_radars):
        print("Invalid Selection")
    else:
        break

#Create and navigate to directory to download
os.chdir(".\\cases\\")
os.mkdir(str(choice))
os.chdir(".\\"+str(choice)+"\\")
with open('.gitkeep', 'w') as fp:
    pass

#Download Necessary Files
for site in sites:
    os.mkdir(site)
    os.chdir(".\\"+site+"\\")
    download_radar_data(site=site, begin=begin_time, end=end_time)
    os.chdir("..\\")
