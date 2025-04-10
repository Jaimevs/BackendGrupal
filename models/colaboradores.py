from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

#modelo para la tabla de colaboradores

class Colaborador(Base):
    __tablename__ = "tbb_colaboradores"
    
    
    ID = Column(Integer, primary_key=True, autoincrement=True, index=True)
    Usuario_Roles_ID = Column(Integer, ForeignKey('tbd_usuarios_roles.Usuario_ID'), unique=True)  # en lugar de persona a usuario roles
    Horario_ID = Column(Integer, ForeignKey('tbb_horarios.ID'))  # Relación con TbbHorarios
    Especialidad = Column(String(50), nullable=True) #verificar si si o no o las opciomes
    Estatus = Column(Boolean, default=True)  
    Fecha_Registro = Column(DateTime, nullable=False)
    Fecha_Actualizacion = Column(DateTime, nullable=False)

    #relaciones
    usuario_rol = relationship("UsuarioRol", back_populates="colaborador")
    horario = relationship("TbbHorarios", back_populates="colaboradores")
