from sqlalchemy import Column, Integer, Text, Enum, DateTime, ForeignKey
from config.db import Base
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

    ID = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    Usuario_Roles_ID = Column(Integer, ForeignKey('tbd_usuarios_roles.Usuario_ID'), nullable=False)
    Sucursal_ID = Column(Integer, nullable=False)# la tabla de sucursales no existe aun, por lo que no se relaciona
    Descripcion = Column(Text, nullable=False)
    Tipo = Column(Enum(TipoQueja), nullable=False, default=TipoQueja.sugerencia)
    Respuesta = Column(Text, nullable=True)
    Estatus = Column(Enum(EstatusQueja), nullable=False, default=EstatusQueja.pendiente)
    Fecha_Registro = Column(DateTime, default=datetime.now, nullable=False)
    Fecha_Actualizacion = Column(DateTime, onupdate=datetime.now, nullable=True)

    # Relaciones adicionales definidas:
    usuario_rol = relationship("UsuarioRol", back_populates="quejas_sugerencias")
    # sucursal = relationship("Sucursal", back_populates="quejas_sugerencias")
