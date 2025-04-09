from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT
from config.db import Base
import models.sucursales
from datetime import datetime

class Instalacion(Base):
    __tablename__ = 'tbb_instalaciones'
    
    Id = Column(Integer, primary_key=True, index=True)
    #Sucursal_Id = Column(Integer, ForeignKey('tbc_sucursales.Id'), nullable=False)
    Descripcion = Column(LONGTEXT)
    Tipo = Column(String(50))
    # Horario_Id = Column(Integer)  # Comentado según solicitud
    # Servicio_Id = Column(Integer)  # Comentado según solicitud
    Observaciones = Column(String(100))
    Estatus = Column(Boolean, default=False)
    Fecha_Registro = Column(DateTime, default=func.now(), nullable=False)
    Fecha_Actualizacion = Column(DateTime, nullable=True,onupdate=datetime.utcnow)
