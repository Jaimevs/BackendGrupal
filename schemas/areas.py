from pydantic import BaseModel
from datetime import datetime 
from typing import Optional


class AreaBase(BaseModel):
    Nombre: str
    Descripcion: Optional[str] = None
    Sucursal_ID: int  # Hice este campo obligatorio según el modelo SQLAlchemy
    Estatus: bool = True  # Hice este campo no opcional con valor por defecto

class AreaCreate(AreaBase):
    pass

class AreaUpdate(BaseModel):  # Cambié la herencia para no requerir todos los campos en actualización
    Nombre: Optional[str] = None
    Descripcion: Optional[str] = None
    Sucursal_ID: Optional[int] = None
    Estatus: Optional[bool] = None

class AreaResponse(AreaBase):
    ID: int
    Fecha_Registro: datetime
    Fecha_Actualizacion: Optional[datetime] = None  # Puede ser null al crear

    class Config:
        from_attributes = True  # Actualizado para Pydantic v2 (antes orm_mode)