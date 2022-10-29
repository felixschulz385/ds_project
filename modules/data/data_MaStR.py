from pickle import TRUE
import requests

PVA_URL = "https://ds.marktstammdatenregister.dev/Marktstammdatenregister/EinheitSolar.csv?_labels=on&_size=max"
WKA_URL = "https://ds.marktstammdatenregister.dev/Marktstammdatenregister/EinheitWind.csv?_labels=on&_size=max"

PVA = requests.get(PVA_URL, stream=True)
WKA = requests.get(WKA_URL, stream=True)

with open("PVA.csv", "wb") as csv:
    for chunk in PVA.iter_content(chunk_size = 1024):
        if chunk:
            csv.write(chunk)
            
with open("WKA.csv", "wb") as csv:
    for chunk in WKA.iter_content(chunk_size = 1024):
        if chunk:
            csv.write(chunk)