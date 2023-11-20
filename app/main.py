import requests
import json
from dotenv import load_dotenv
import os
from models.model import Model
load_dotenv()

API_KEY=os.environ.get("VEGVESEN_API_KEY")
VEGVESEN_URL=os.environ.get("VEGVESEN_URL")

kjennemerke="DP24034"

def main():
    session = requests.Session()
    session.params.update({'kjennemerke':kjennemerke})
    session.headers.update({'SVV-Authorization': f"Apikey {API_KEY}"})
    response=session.get(VEGVESEN_URL)
    kjoretoy_json=response.json()
    with open(f"output/{kjennemerke}.json","w") as f:
        f.write(json.dumps(kjoretoy_json, indent=4,ensure_ascii=False))
    kjoretoy=Model(**kjoretoy_json).kjoretoydataListe[0]
    kontrollfrist=kjoretoy.periodiskKjoretoyKontroll.kontrollfrist
    merke=kjoretoy.godkjenning.tekniskGodkjenning.tekniskeData.generelt.merke[0].merke
    modell=kjoretoy.godkjenning.tekniskGodkjenning.tekniskeData.generelt.handelsbetegnelse[0]
    kw=kjoretoy.godkjenning.tekniskGodkjenning.tekniskeData.motorOgDrivverk.motor[0].drivstoff[0].maksNettoEffekt
    print(F"{kjennemerke=}, {merke=}, {modell=}, {kw=}, {kontrollfrist=}")

if __name__ == "__main__":
    main()