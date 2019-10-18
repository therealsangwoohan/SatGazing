import pandas as pd
import sys
import requests


def visualPasses(satId: int, lat: float, lng: float, alt: float, days: int,
                 seconds: int, apiKey: str) -> pd.DataFrame:
    request = requests.get("http://www.n2yo.com/rest/v1/" +
                           "satellite/visualpasses/" +
                           satID + "/" +
                           lat + "/" +
                           lng + "/" +
                           alt + "/" +
                           days + "/" +
                           seconds + "/&apiKey=" +
                           apiKey)
    request_json = request.json()
    passes = request_json["passes"]
    d = {}
    for key in passes[0]:
        d[key] = tuple(d[key] for d in passes)
    return pd.DataFrame.from_dict(d)


if __name__ == "__main__":
    nA = len(sys.argv)
    satID = sys.argv[nA - 7]
    lat = sys.argv[nA - 6]
    lng = sys.argv[nA - 5]
    alt = sys.argv[nA - 4]
    days = sys.argv[nA - 3]
    seconds = sys.argv[nA - 2]
    apiKey = sys.argv[nA - 1]
    df = visualPasses(satID, lat, lng, alt, days, seconds, apiKey)
    print(df[["startUTC", "endUTC", "startAz", "endAz", "startEl", "endEl"]])
