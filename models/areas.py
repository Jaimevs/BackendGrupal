from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Areas(Base):
    __tablename__ = "tbb_areas"

    ID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Nombre = Column(String(80))
    Descripcion = Column(String(80))
    Sucursal_ID = Column(Integer, ForeignKey('tbc_sucursales.ID'))
    Estatus = Column(Boolean, default=True)  
    Fecha_Registro = Column(DateTime, default=datetime.utcnow)
    Fecha_Actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sucursal = relationship('TbcSucursales', backref='areas')
    