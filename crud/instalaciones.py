from sqlalchemy.orm import Session
from models.instalaciones import Instalacion
from schemas.instalaciones import InstalacionCreate, InstalacionUpdate

# Crear una instalación
def create_instalacion(db: Session, instalacion: InstalacionCreate):
    db_instalacion = Instalacion(**instalacion.dict())
    db.add(db_instalacion)
    db.commit()
    db.refresh(db_instalacion)
    return db_instalacion

# Obtener todas las instalaciones
def get_instalaciones(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Instalacion).offset(skip).limit(limit).all()

# Obtener una instalación por ID
def get_instalacion(db: Session, instalacion_id: int):
    return db.query(Instalacion).filter(Instalacion.Id == instalacion_id).first()

# Actualizar una instalación
def update_instalacion(db: Session, instalacion_id: int, instalacion: InstalacionUpdate):
    db_instalacion = db.query(Instalacion).filter(Instalacion.Id == instalacion_id).first()
    if not db_instalacion:
        return None
    for key, value in instalacion.dict(exclude_unset=True).items():
        setattr(db_instalacion, key, value)
    db.commit()
    db.refresh(db_instalacion)
    return db_instalacion

# Eliminar una instalación
def delete_instalacion(db: Session, instalacion_id: int):
    db_instalacion = db.query(Instalacion).filter(Instalacion.Id == instalacion_id).first()
    if not db_instalacion:
        return None
    db.delete(db_instalacion)
    db.commit()
    return db_instalacion
