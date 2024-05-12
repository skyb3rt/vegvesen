from fastapi import FastAPI, status
import fastapi
from db.services import get_all_cars, get_db, new_car
import sqlalchemy.orm as _orm
from db import schemas
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
app = FastAPI()


@app.get("/car/{kjennemerke}", status_code=status.HTTP_200_OK, response_model=schemas.Car)
def read_items(kjennemerke:str, db: _orm.Session = fastapi.Depends(get_db)):
    return new_car(db=db,kjennemerke=kjennemerke)


@app.get("/cars/all", response_model=List[schemas.Car])
def get_all_items(db: _orm.Session = fastapi.Depends(get_db)):
    return get_all_cars(db=db)
