from json import JSONDecodeError
from typing import Dict


from db.schemas import Car
from db.database import engine
from db.database import SessionLocal
import requests
import json
from dotenv import load_dotenv
import os
from models.model import Model

load_dotenv()

VEGVESEN_API_KEY = os.environ.get("VEGVESEN_API_KEY")
VEGVESEN_URL = os.environ.get("VEGVESEN_URL")

kjennemerker = ["DP24034", "DN14328", "ZH16781", "HJ74037", "DF81666"]


def get_car_info(kjennemerke: str) -> Car | dict[str, str] | dict[str, str]:
    session = requests.Session()
    session.headers.update({'SVV-Authorization': f"Apikey {VEGVESEN_API_KEY}"})
    session.params.update({'kjennemerke': kjennemerke})
    response = session.get(VEGVESEN_URL)

    try:
        kjoretoy_json = response.json()
        kjoretoy = Model(**kjoretoy_json).kjoretoydataListe[0]
        kontrollfrist = kjoretoy.periodiskKjoretoyKontroll.kontrollfrist
        merke = kjoretoy.godkjenning.tekniskGodkjenning.tekniskeData.generelt.merke[0].merke
        modell = kjoretoy.godkjenning.tekniskGodkjenning.tekniskeData.generelt.handelsbetegnelse[0]
        kw = kjoretoy.godkjenning.tekniskGodkjenning.tekniskeData.motorOgDrivverk.motor[0].drivstoff[0].maksNettoEffekt
        registreringsstatus = kjoretoy.registrering.registreringsstatus.kodeBeskrivelse
        return Car(id=kjennemerke, registreringsstatus=registreringsstatus, merke=merke, modell=modell,
                   kontrollfrist=kontrollfrist or "ukjent", info=kjoretoy_json)
    except AttributeError:
        return dict(kjennemerke=kjennemerke, info="feil ved henting av info")
    except JSONDecodeError:
        return dict(kjennemerke=kjennemerke, info="feil ved henting av info")


if __name__ == "__main__":
    print(get_car_info(kjennemerke=kjennemerker[0]))
