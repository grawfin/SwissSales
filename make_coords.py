import pandas as pd
import requests
import json

df = pd.read_csv("sample.csv",on_bad_lines='skip',sep='\t')
url = "http://geodesy.geo.admin.ch/reframe/lv95towgs84"

E = list(df['GKODE'])
N = list(df['GKODN'])

lats = []
lngs = []

for i in range(len(E)):
    try:
        par = {"easting":str(E[i]), "northing":str(N[i])}
        print(par)
        response = requests.get(url, params=par)
        print(response.text)
        res = json.loads(response.text)['coordinates']
    except:
        res = [None, None]
    lats.append(res[0])
    lngs.append(res[1])


df['lat'] = lats
df['long'] = lngs

df.to_csv("sample2.csv", index=False)
