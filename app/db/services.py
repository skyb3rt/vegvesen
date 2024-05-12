import json

from db import database
from db.db_models import Car
import sqlalchemy.orm as _orm
from dotenv import load_dotenv
from db.model import Model
import os

from requests import JSONDecodeError, Session

load_dotenv()

VEGVESEN_API_KEY = os.environ.get("VEGVESEN_API_KEY")
VEGVESEN_URL = os.environ.get("VEGVESEN_URL")


def get_db() -> _orm.session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_all_cars(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(Car).offset(skip).limit(limit).all()


def new_car(db: _orm.Session, kjennemerke):
    car = get_car_info(kjennemerke)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


def get_car_info(kjennemerke: str) -> Car | dict[str, str] | dict[str, str]:
    session = Session()
    session.headers.update({'SVV-Authorization': f"Apikey {VEGVESEN_API_KEY}"})
    session.params.update({'kjennemerke': kjennemerke})
    response = session.get(VEGVESEN_URL)

    try:
        kjoretoy_json = response.json()
        kjoretoy = Model(**kjoretoy_json).kjoretoydataListe[0]
        kontrollfrist = kjoretoy.periodiskKjoretoyKontroll.kontrollfrist
        merke = kjoretoy.godkjenning.tekniskGodkjenning.tekniskeData.generelt.merke[0].merke
        modell = kjoretoy.godkjenning.tekniskGodkjenning.tekniskeData.generelt.handelsbetegnelse[0]
        registreringsstatus = kjoretoy.registrering.registreringsstatus.kodeBeskrivelse
        return Car(id=kjennemerke, registreringsstatus=registreringsstatus, merke=merke, modell=modell,
                   kontrollfrist=kontrollfrist or "ukjent", info=json.dumps(kjoretoy_json))
    except AttributeError:
        return dict(kjennemerke=kjennemerke, info="feil ved henting av info")
    except JSONDecodeError:
        return dict(kjennemerke=kjennemerke, info="feil ved henting av info")
