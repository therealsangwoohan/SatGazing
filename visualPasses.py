from pprint import pprint
import numpy as np
import pandas as pd
import requests
import json

def convertSearch2Coord(search):
    url = "https://us1.locationiq.com/v1/search.php"
    data = {
        'key': 'pk.86c36508e5bda29ff74b4fe11de36d96',
        'q': search,
        'format': 'json'
    }
    response = requests.get(url, params=data)
    res = response.text
    d = json.loads(res)
    return d[0]
# print(response.text)

def visualPasses(satId_list, lat, lon, alt, days, seconds, apiKey):
    bigDF = pd.DataFrame()
    descriptions = json.load(open("descriptions.json"))
    launchDates = json.load(open("launchDates.json"))
    for satID in satID_list:
        request = requests.get("http://www.n2yo.com/rest/v1/" +
                               "satellite/visualpasses/" +
                               str(satID) + "/" +
                               str(lat) + "/" +
                               str(lon) + "/" +
                               str(alt) + "/" +
                               str(days) + "/" +
                               str(seconds) + "/&apiKey=" +
                               apiKey)
        request_json = request.json()
        satname = (request_json["info"])["satname"]
        description = descriptions[satname]
        launchDate = launchDates[satname]
        try:
            passes = request_json["passes"]
        except Exception:
            print("No passes for:", satname)
            continue
        d = {}
        for key in passes[0]:
            d[key] = tuple(d[key] for d in passes)
        df = pd.DataFrame.from_dict(d)
        df = df[["startUTC", "endUTC", "duration", "startAz", "endAz",
                 "startEl", "endEl"]]
        df['startUTC'] = pd.to_datetime(df['startUTC'], unit='s')
        df['endUTC'] = pd.to_datetime(df['endUTC'], unit='s')
        df = df.rename(columns={"startUTC": "startTime", "endUTC": "endTime"})
        df["description"] = description
        df["launchDate"] = launchDate
        df["satname"] = satname
        df = df.set_index("satname")
        bigDF = bigDF.append(df)
    bigDF = bigDF.sort_values('startTime')
    bigDF = bigDF.reset_index()
    bigDF['startTime'] = bigDF['startTime'].astype(str)
    bigDF['endTime'] = bigDF['endTime'].astype(str)
    return bigDF


if __name__ == "__main__":
    d = convertSearch2Coord("Ecole Polytechnique montreal")
    df = pd.read_csv("Popid.csv", delimiter=',', header=None)
    satID_list = list(np.transpose(df.values)[0])
    lat = d["lat"]
    lon = d["lon"] 
    alt = 0
    days = 1
    seconds = 1
    apiKey = "HF5J3Q-L52Z93-EBH98V-47RW"
    df = visualPasses(satID_list, lat, lon, alt, days, seconds, apiKey)
    parsed = json.loads(df.to_json(orient='index'))
    json.dump(parsed, open("output.json", 'w'))
