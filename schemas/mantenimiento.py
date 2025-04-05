from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# Esquema Pydantic para Equipamiento (no el modelo SQLAlchemy)
class EquipamientoBase(BaseModel):
    Id: int
    Nombre: str

    class Config:
        orm_mode = True

class MantenimientoBase(BaseModel):
    Id_equipamiento: int  # Referencia al equipamiento
    Descripcion: str
    Responsable: str
    Costo: int
    Estatus: bool
    Fecha_mantenimiento: datetime
    Fecha_Actualizacion: datetime

class MantenimientoCreate(MantenimientoBase):
    pass

class MantenimientoUpdate(MantenimientoBase):
    pass

class Mantenimiento(MantenimientoBase):
    Id: int
    equipamiento: Optional[EquipamientoBase]  # Usar un esquema Pydantic en lugar del modelo SQLAlchemy

    class Config:
        orm_mode = True
