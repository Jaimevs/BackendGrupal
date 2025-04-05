from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, DECIMAL
from sqlalchemy.orm import relationship
from config.db import Base
from datetime import datetime

class Producto(Base):
    __tablename__ = "tbb_productos"
    
    ID = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Marca = Column(String(100), nullable=False)
    Cantidad = Column(Integer, default=0)
    Cod_barras = Column(String(50), unique=True, nullable=False)
    Descripcion = Column(String(255))
    Presentacion = Column(String(100))
    Precio_actual = Column(DECIMAL(6,2), nullable=False)
    Fotografia = Column(String(100))
    Estatus = Column(Boolean, default=False)
    Fecha_Registro = Column(DateTime, default=func.now(), nullable=False)  # CURRENT_TIMESTAMP
    Fecha_Actualizacion = Column(DateTime, nullable=True, onupdate=datetime.utcnow) 