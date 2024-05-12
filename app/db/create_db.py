from sqlmodel import SQLModel
from db_models import Car
from database import engine
import logging

logging.info("Creating Database")

SQLModel.metadata.create_all(engine)