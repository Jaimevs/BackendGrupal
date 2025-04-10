from sqlalchemy.orm import Session
from models.areas import Areas
from schemas.areas import AreaCreate, AreaUpdate, AreaResponse
from fastapi import HTTPException, status
from datetime import datetime

# Función para crear un nuevo área
def create_area(db: Session, area: AreaCreate):
    db_area = Areas(
        Nombre=area.Nombre,
        Descripcion=area.Descripcion,
        Sucursal_ID=area.Sucursal_ID,
        Estatus=True,  # Valor por defecto según modelo
        Fecha_Registro=datetime.now(),
        Fecha_Actualizacion=datetime.now()
    )
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

# Función para obtener todos los áreas
def All_areas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Areas).offset(skip).limit(limit).all()

# Función para actualizar un área
def update_area(db: Session, area_id: int, area_data: AreaUpdate):
    db_area = db.query(Areas).filter(Areas.ID == area_id).first()
    if not db_area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Área no encontrada")
    
    update_data = area_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_area, key, value)
    
    db_area.Fecha_Actualizacion = datetime.now()
    db.commit()
    db.refresh(db_area)
    return db_area

# Función para eliminar un área
def delete_area(db: Session, area_id: int):
    db_area = db.query(Areas).filter(Areas.ID == area_id).first()
    if not db_area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Área no encontrada")
    
    db.delete(db_area)
    db.commit()
    return db_area

# Función para obtener un área por ID
def get_area_by_id(db: Session, area_id: int):
    db_area = db.query(Areas).filter(Areas.ID == area_id).first()
    if not db_area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Área no encontrada")
    return db_area