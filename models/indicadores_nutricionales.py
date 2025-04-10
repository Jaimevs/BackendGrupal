from sqlalchemy import Column, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from sqlalchemy.sql import func
from config.db import Base

class NivelActividad(enum.Enum):
    Sedentario = "Sedentario"
    Ligero = "Ligero"
    Moderado = "Moderado"
    Activo = "Activo"
    Muy_Activo = "Muy_Activo"

class IndicadorNutricional(Base):
    __tablename__ = "tbd_indicadores_nutricionales"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    altura = Column(Float, nullable=False)
    peso = Column(Float, nullable=False)
    imc = Column(Float, nullable=False)
    porcentaje_grasa = Column(Float, nullable=False)
    nivel_actividad = Column(Enum(NivelActividad), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow, server_default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    
    # Cambiando la referencia para usar ID en mayúsculas
    usuario_id = Column(Integer, ForeignKey("tbb_usuarios.ID"), nullable=True)
    
    # Asumiendo que la clase se llama User en tu aplicación
    usuario = relationship("User", back_populates="indicadores_nutricionales")