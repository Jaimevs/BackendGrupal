from fastapi import APIRouter,HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import json
import crud.mantenimiento, config.db, schemas.mantenimiento, models.mantenimiento
from typing import List
from jwt_config import solicita_token 
from portadortoken import Portador
from schemas.mantenimiento import Mantenimiento as MantenimientoSchema
from fastapi.encoders import jsonable_encoder

key = Fernet.generate_key()
f = Fernet(key)

mantenimiento = APIRouter()
models.mantenimiento.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Ruta de bienvenida
@mantenimiento.get('/')
def bienvenido():
    return 'Bienvenido al sistema de APIs'

# Ruta para obtener todos los mantenimientos
@mantenimiento.get('/mantenimiento/', response_model=List[schemas.mantenimiento.Mantenimiento],tags=['Mantenimiento'], dependencies=[Depends(Portador())])
def read_mantenimiento(skip: int=0, limit: int=10, db: Session=Depends(get_db)):
    db_mantenimiento = crud.mantenimiento.get_mantenimientos(db=db,skip=skip, limit=limit)
    return db_mantenimiento

# Ruta para obtener un mantenimiento por ID
@mantenimiento.post("/mantenimiento/{id}", response_model=schemas.mantenimiento.Mantenimiento, tags=["Mantenimiento"], dependencies=[Depends(Portador())])
def read_mantenimiento(id: int, db: Session = Depends(get_db)):
    db_mantenimiento = crud.mantenimiento.get_mantenimiento_by_mantenimiento(db=db, id_equipamiento=id)
    if db_mantenimiento is None:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return db_mantenimiento  # ⬅️ Convertir a esquema Pydantic

# Ruta para crear un mantenimiento
@mantenimiento.post('/mantenimiento/', response_model=schemas.mantenimiento.Mantenimiento, tags=['Mantenimiento'], dependencies=[Depends(Portador())])
def create_mantenimiento(mantenimiento: schemas.mantenimiento.MantenimientoCreate, db: Session=Depends(get_db)):
    db_mantenimiento = crud.mantenimiento.get_mantenimiento_by_mantenimiento(db, mantenimiento.Id_equipamiento)  
    if db_mantenimiento:
        raise HTTPException(status_code=400, detail="Hay un mantenimiento en proceso para este equipamiento")

    return crud.mantenimiento.create_mantenimiento(db=db, mantenimiento=mantenimiento)


# Ruta para actualizar un mantenimiento
@mantenimiento.put('/mantenimiento/{id}', response_model=schemas.mantenimiento.Mantenimiento,tags=['Mantenimiento'], dependencies=[Depends(Portador())])
def update_mantenimiento(id:int,mantenimiento: schemas.mantenimiento.MantenimientoUpdate, db: Session=Depends(get_db)):
    db_mantenimiento = crud.mantenimiento.update_mantenimiento(db=db, id=id, mantenimiento=mantenimiento)
    if db_mantenimiento is None:
        raise HTTPException(status_code=404, detail="El mantenimiento no existe, no se pudo actualizar ")
    return db_mantenimiento

# Ruta para eliminar un mantenimiento
@mantenimiento.delete("/mantenimiento/{id}", tags=["Mantenimiento"])
def delete_mantenimiento(id: int, db: Session = Depends(get_db)):
    db_mantenimiento = crud.mantenimiento.delete_mantenimiento(db, id)
    if not db_mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    
    crud.mantenimiento.delete_mantenimiento(db, id)  # Aquí eliminas el mantenimiento

    return {"message": "Mantenimiento eliminado correctamente"}


