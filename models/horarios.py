from sqlalchemy import Column, Integer, Enum, Time, DateTime, SmallInteger, ForeignKey
from database import Base

import enum


class TipoHorario(enum.Enum):
    matutino = "matutino"
    vespertino = "vespertino"
    especial = "especial"

class TbbHorarios(Base):
    __tablename__ = 'tbb_horarios'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Tipo = Column(Enum(TipoHorario), nullable=False)
    Hora_Inicio = Column(Time, nullable=False)
    Hora_Fin = Column(Time, nullable=False)
    Fecha_Registro = Column(DateTime, nullable=False)
    Fecha_Actualizacion = Column(DateTime, nullable=False)
    Estatus = Column(SmallInteger, nullable=False,default=1)


