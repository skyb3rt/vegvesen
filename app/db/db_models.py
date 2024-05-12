from typing import Optional
from sqlmodel import Field, SQLModel,JSON,Column
from pydantic import Json
import json

class Car(SQLModel, table=True):
    __tablename__ = "vegvesen"
    id: Optional[str]=Field(default=None, primary_key=True,nullable=False,index=True)
    registreringsstatus: Optional[str]=Field(default=None,nullable=True)
    merke: Optional[str]=Field(default=None,nullable=True)
    modell: Optional[str]=Field(default=None,nullable=True)
    kontrollfrist: Optional[str]=Field(default=None,nullable=True)
    info: Optional[Json]=Field(sa_column=Column(JSON),default={})