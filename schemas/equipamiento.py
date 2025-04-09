from typing import List, Union, Optional
from pydantic  import BaseModel
from datetime import datetime

class EquipamientoBase(BaseModel):
    Nombre : str 
    Marca : str 
    Modelo : str
    Fotografia: str
    Estatus : bool
    Total_Existencias : int
    Fecha_Registro :datetime
    Fecha_Actualizacion :datetime
     
     
class EquipamientoCreate(EquipamientoBase):
    pass

class EquipamientoUpdate(EquipamientoBase):
    pass

class Equipamiento(EquipamientoBase):
    Id:int
    
    class Config:
        orm_mode = True
