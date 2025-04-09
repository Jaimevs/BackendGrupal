from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InstalacionBase(BaseModel):
    #Sucursal_Id: int  # Llave foránea a sucursales
    Descripcion: str
    Tipo: str
    # Horario_Id: Optional[int]  # Comentado según solicitud
    # Servicio_Id: Optional[int]  # Comentado según solicitud
    Observaciones: Optional[str] = None
    Estatus: Optional[bool] = False

class InstalacionCreate(InstalacionBase):
    pass

class InstalacionUpdate(BaseModel):
    #Sucursal_Id: Optional[int] = None
    Descripcion: Optional[str] = None
    Tipo: Optional[str] = None
    # Horario_Id: Optional[int] = None  # Comentado según solicitud
    # Servicio_Id: Optional[int] = None  # Comentado según solicitud
    Observaciones: Optional[str] = None
    Estatus: Optional[bool] = None

class InstalacionResponse(InstalacionBase):
    Id: int
    Fecha_Registro: datetime
    Fecha_Actualizacion: Optional[datetime] = None

    class Config:
        orm_mode = True
