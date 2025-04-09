from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional
from enum import Enum

class TipoHorarioEnum(str, Enum):
    matutino = "matutino"
    vespertino = "vespertino"
    especial = "especial"

class TbbHorariosBase(BaseModel):
    Tipo: TipoHorarioEnum
    Hora_Inicio: time
    Hora_Fin: time
    Estatus: int = 1

    class Config:
        orm_mode = True

# Al crear un nuevo horario, no se incluyen las fechas de registro y actualización
class TbbHorariosCreate(TbbHorariosBase):
    pass

# Para la actualización, el ID es opcional y tampoco incluye las fechas
class TbbHorariosUpdate(TbbHorariosBase):
    ID: Optional[int] = None

# Para la representación final, se incluyen las fechas
class TbbHorarios(TbbHorariosBase):
    ID: int
    Fecha_Registro: datetime
    Fecha_Actualizacion: datetime
