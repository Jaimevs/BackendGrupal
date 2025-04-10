from sqlalchemy import Boolean, Column, Enum, Float, Integer, Text, DateTime, String
import datetime
from config.db import Base
import enum

class ObjetivoDieta(enum.Enum):
    Perdida_de_Peso = "Perdida de Peso"
    Aumento_de_Masa_Muscular = "Aumento de masa muscular"
    Mantenimiento = "Mantenimiento"

class TipoEjercicioRecomendado(enum.Enum):
    Cardio = "Cardio"
    Levantamiento_de_Pesas = "Levantamiento de pesas"
    Ejercicios_Tecnicos = "Ejercicios Tecnicos"

class DiasEjercicio(enum.Enum):
    Un_Dia = "1 dia a la semana"
    Dos_Dias = "2 dias a la semana"
    Tres_Dias = "3 dias a la semana"
    Cuatro_Dias = "4 dias a la semana"
    Cinco_Dias = "5 dias a la semana"

class Dieta(Base):
    __tablename__ = "tbc_dietas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(55), nullable=False)
    objetivo = Column(Enum(ObjetivoDieta), nullable=False)
    tipo_ejercicios_recomendados = Column(Enum(TipoEjercicioRecomendado), nullable=False)
    dias_ejercicio = Column(Enum(DiasEjercicio), nullable=False)
    calorias_diarias = Column(Float, nullable=False)
    observaciones = Column(Text, nullable=True)
    estatus = Column(Boolean, default=True, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=True)
