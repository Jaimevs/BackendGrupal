
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from config.db import Base
from datetime import datetime

class Mantenimiento(Base):
    __tablename__ = "tbb_mantenimiento"

    Id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Id_equipamiento = Column(Integer, ForeignKey("tbb_equipamientos.Id"), nullable=False)  # Relación con Equipamiento
    Descripcion = Column(String(100), nullable=False)
    Responsable = Column(String(100), nullable=False)
    Costo = Column(Integer, nullable=False)
    Estatus = Column(Boolean, default=True)
    Fecha_mantenimiento = Column(DateTime,default=func.now(), nullable=False)
    Fecha_Actualizacion = Column(DateTime, nullable=False, onupdate=datetime.utcnow)

    equipamiento = relationship("Equipamiento", back_populates="mantenimientos")  # <-- Relación ORM


