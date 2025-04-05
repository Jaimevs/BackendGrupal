from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT
from config.db import Base
from datetime import datetime




class Sucursal(Base):
    __tablename__ = 'tbc_sucursales'
    Id = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(60))
    Direccion = Column(String(150))
    Responsable_Id = Column(Integer)
    Total_Clientes_Atendidos =Column(Integer, default=0)
    Promedio_Clientes_X_Dia = Column(Integer , default=0)
    Capacidad_Maxima = Column (Integer , default=0)
    Total_Empleados = Column (Integer, default=0)
    Horario_Disponibilidad = Column (LONGTEXT)
    Estatus = Column(Boolean, default=False)
    Fecha_Registro = Column(DateTime, default=datetime.utcnow, nullable=False)
    Fecha_Actualizacion = Column(DateTime, onupdate=datetime.utcnow)
    
    
    
    
