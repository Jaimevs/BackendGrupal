from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey, Enum
from database import Base
from datetime import datetime
import enum
from sqlalchemy.orm import relationship

class TipoQueja(enum.Enum):
    sugerencia = "sugerencia"
    queja = "queja"
    reclamo = "reclamo"

class EstatusQueja(enum.Enum):
    respondida = "respondida"
    pendiente = "pendiente"
    archivada = "archivada"

class QuejasSugerencias(Base):
    __tablename__ = "tbd_quejas_sugerencias"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Usuario_Roles_ID = Column(Integer, ForeignKey('tbd_usuarios_roles.ID'), unique=True)  
    Sucursal_ID = Column(Integer, ForeignKey('tbc_sucursales.ID'),unique=True )
    Descripcion = Column(Text, nullable=False)  # Campo obligatorio
    Tipo = Column(Enum(TipoQueja), nullable=False, default="sugerencia")  # Campo obligatorio
    Respuesta = Column(Text, nullable=True)  
    Estatus = Column(Enum(EstatusQueja), nullable=False, default="espera")
    Fecha_registro = Column(DateTime, nullable=False)
    Fecha_actualizacion = Column(DateTime, nullable=False)

