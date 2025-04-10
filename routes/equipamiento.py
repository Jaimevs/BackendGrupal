from fastapi import APIRouter,HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import json
import crud.equipamiento, config.db, schemas.equipamiento, models.equipamiento
from typing import List
from jwt_config import solicita_token 
from portadortoken import Portador

key = Fernet.generate_key()
f = Fernet(key)

equipamiento = APIRouter()
models.equipamiento.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Ruta de bienvenida
@equipamiento.get('/')
def bienvenido():
    return 'Bienvenido al sistema de APIs'

# Ruta para obtener todos los equipamientos
@equipamiento.get('/equipamiento/', response_model=List[schemas.equipamiento.Equipamiento],tags=['Equipamiento'], dependencies=[Depends(Portador())])
def read_equipamiento(skip: int=0, limit: int=10, db: Session=Depends(get_db)):
    db_equipamiento = crud.equipamiento.get_equipamientos(db=db,skip=skip, limit=limit)
    return db_equipamiento

# Ruta para obtener un equipamiento por ID
@equipamiento.post("/equipamiento/{id}", response_model=schemas.equipamiento.Equipamiento, tags=["Equipamiento"], dependencies=[Depends(Portador())])
def read_equipamiento(id: int, db: Session = Depends(get_db)):
    db_equipamiento= crud.equipamiento.get_equipamiento(db=db, id=id)
    if db_equipamiento is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_equipamiento

# Ruta para crear un equipamiento
@equipamiento.post('/equipamiento/', response_model=schemas.equipamiento.EquipamientoCreate,tags=['Equipamiento'], dependencies=[Depends(Portador())])
def create_equipamiento(equipamiento: schemas.equipamiento.EquipamientoCreate, db: Session=Depends(get_db)):
    db_equipamiento = crud.equipamiento.get_equipamiento_by_equipamiento(db,equipamiento=equipamiento.Nombre)
    if db_equipamiento:
        raise HTTPException(status_code=400, detail="Equipamiento existente intenta nuevamente")
    return crud.equipamiento.create_equipamiento(db=db, equipamiento=equipamiento)

# Ruta para actualizar un equipamiento
@equipamiento.put('/equipamiento/{id}', response_model=schemas.equipamiento.Equipamiento,tags=['Equipamiento'], dependencies=[Depends(Portador())])
def update_equipamiento(id:int,equipamiento: schemas.equipamiento.EquipamientoUpdate, db: Session=Depends(get_db)):
    db_equipamiento = crud.equipamiento.update_equipamiento(db=db, id=id, equipamiento=equipamiento)
    if db_equipamiento is None:
        raise HTTPException(status_code=404, detail="Equipamiento no existe, no se pudo actualizar ")
    return db_equipamiento

# Ruta para eliminar un equipamiento
@equipamiento.delete('/equipamiento/{id}', response_model=schemas.equipamiento.Equipamiento,tags=['Equipamiento'], dependencies=[Depends(Portador())])
def delete_equipamiento(id:int, db: Session=Depends(get_db)):
    db_equipamiento = crud.equipamiento.delete_equipamiento(db=db, id=id)
    if db_equipamiento is None:
        raise HTTPException(status_code=404, detail="Sucursal no existe, no se pudo eliminar ")
    return db_equipamiento
