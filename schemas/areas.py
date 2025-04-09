from pydantic import BaseModel
from datetime import datetime 
from typing import Optional


class AreaBase(BaseModel):
    Nombre: str
    Descripcion: Optional[str] = None
    Estatus: Optional[bool] = True  # 1 para 'activo', 0 para 'inactivo'
    Sucursal_ID: Optional[int] = None  # ID de la sucursal asociada

class AreaCreate(AreaBase):
    pass

class AreaUpdate(AreaBase):
    ID: Optional[int] = None

class AreaResponse(AreaBase):
    ID: int
    Fecha_Registro: datetime
    Fecha_Actualizacion: datetime

    class Config:
        orm_mode = True