from pprint import pprint
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import requests
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    location = request.form.get("location")
    d = convertSearch2Coord(location)
    df = pd.read_csv("Popid.csv", delimiter=',', header=None)
    satID_list = list(np.transpose(df.values)[0])
    lat = d["lat"]
    lon = d["lon"]
    alt = 0
    days = 1
    seconds = 1
    apiKey = "HF5J3Q-L52Z93-EBH98V-47RW"
    df = visualPasses(satID_list, lat, lon, alt, days, seconds, apiKey)
    print(df)
    parsed = json.loads(df.to_json(orient='index'))
    print(json.dumps(parsed, indent=4, sort_keys=True))
    return render_template("index.html")


def convertSearch2Coord(search: str):
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

def visualPasses(satId_list: list, lat: float, lon: float, alt: float,
                 days: int, seconds: int, apiKey: str) -> pd.DataFrame:
    bigDF = pd.DataFrame()
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
        df["satname"] = satname
        df = df.set_index("satname")
        bigDF = bigDF.append(df)
    bigDF = bigDF.sort_values('startTime')
    bigDF = bigDF.reset_index()
    bigDF['startTime'] = bigDF['startTime'].astype(str)
    bigDF['endTime'] = bigDF['endTime'].astype(str)
    return bigDF


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
