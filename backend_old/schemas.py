from pydantic import BaseModel, ConfigDict
from datetime import time, date
from typing import Optional

# Schemas



class Integrity(BaseModel):
    id: int
    hash: str

class Info(BaseModel):
    id: int
    trabajo: str
    ingresos: float
    deudas: float
    credito: float
