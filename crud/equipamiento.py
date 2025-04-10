import models.equipamiento
import schemas.equipamiento
from sqlalchemy.orm import Session
import models, schemas

# Busqueda por id
def get_equipamiento(db:Session, id: int):
    return db.query(models.equipamiento.Equipamiento).filter(models.equipamiento.Equipamiento.Id == id).first()

# Busqueda por equipamiento
def get_equipamiento_by_equipamiento(db:Session, equipamiento : str):
    return db.query(models.equipamiento.Equipamiento).filter(models.equipamiento.Equipamiento.Nombre == equipamiento).first()

# Buscar todos los equipamientos
def get_equipamientos(db:Session, skip: int=0, limit:int=10):
    return db.query(models.equipamiento.Equipamiento).offset(skip).limit(limit).all()

# Crear un nuevo equipamiento
def create_equipamiento(db:Session, equipamiento: schemas.equipamiento.EquipamientoCreate):
    db_equipamiento = models.equipamiento.Equipamiento(
                                             Nombre=equipamiento.Nombre,
                                             Marca=equipamiento.Marca,
                                             Modelo=equipamiento.Modelo,
                                             Fotografia=equipamiento.Fotografia,
                                             Estatus=equipamiento.Estatus,
                                             Total_Existencias=equipamiento.Total_Existencias,
                                             Fecha_Registro=equipamiento.Fecha_Registro,
                                             Fecha_Actualizacion=equipamiento.Fecha_Actualizacion)
    
    
    db.add(db_equipamiento)
    db.commit()
    db.refresh(db_equipamiento)
    print(db_equipamiento)
    return db_equipamiento

# Actualizar un equipamiento por id
def update_equipamiento(db:Session, id:int, equipamiento:schemas.equipamiento.EquipamientoUpdate):
    db_equipamiento = db.query(models.equipamiento.Equipamiento).filter(models.equipamiento.Equipamiento.Id == id).first()
    if db_equipamiento:
        for var, value in vars(equipamiento).items():
            setattr(db_equipamiento, var, value) if value else None
        db.commit()
        db.refresh(db_equipamiento)
    return db_equipamiento

# Eliminar un equipamiento por id
def delete_equipamiento(db:Session, id:int):
    db_equipamiento = db.query(models.equipamiento.Equipamiento).filter(models.equipamiento.Equipamiento.Id == id).first()
    if db_equipamiento:
        db.delete(db_equipamiento)
        db.commit()
    return db_equipamiento