from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
from datetime import datetime

class Areas(Base):
    __tablename__ = "tbb_areas"
    
    ID = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    Nombre = Column(String(80), nullable=False)
    Descripcion = Column(String(80), nullable=True)
    Sucursal_ID = Column(Integer, nullable=False) # aun no se relaciona con la tabla de sucursales
    Estatus = Column(Boolean, default=True, nullable=False)
    Fecha_Registro = Column(DateTime, default=datetime.now, nullable=False)
    Fecha_Actualizacion = Column(DateTime, onupdate=datetime.now, nullable=True)
    
    # Relaciones
    servicios = relationship("Servicios", back_populates="area")
    
    def __repr__(self):
        return f"<Areas(ID={self.ID}, Nombre='{self.Nombre}')>"