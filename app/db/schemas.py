from typing import List,Optional
from pydantic import BaseModel,Json
import json


class Car(BaseModel):
    id: str
    registreringsstatus: Optional[str]
    merke: Optional[str]
    modell:Optional[str]
    kontrollfrist: Optional[str]
    info: Optional[Json]
