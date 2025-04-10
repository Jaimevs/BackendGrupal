from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import crud.instalaciones, config.db, schemas.instalaciones, models.instalaciones
from typing import List
from portadortoken import Portador

instalacion = APIRouter()
models.instalaciones.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta de bienvenida
@instalacion.get('/')
def bienvenido():
    return JSONResponse(content={"message": "Bienvenido al sistema de APIs"})

# Obtener todas las instalaciones
@instalacion.get('/instalacion/', response_model=List[schemas.instalaciones.InstalacionResponse], tags=['Instalacion'], dependencies=[Depends(Portador())])
def read_instalaciones(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.instalaciones.get_instalaciones(db=db, skip=skip, limit=limit)

# Obtener una instalación por ID
@instalacion.get("/instalacion/{id}", response_model=schemas.instalaciones.InstalacionResponse, tags=["Instalacion"], dependencies=[Depends(Portador())])
def read_instalacion(id: int, db: Session = Depends(get_db)):
    instalacion = crud.instalaciones.get_instalacion(db=db, instalacion_id=id)
    if not instalacion:
        raise HTTPException(status_code=404, detail="Instalación no encontrada")
    return instalacion

# Crear una instalación
@instalacion.post('/instalacion/', response_model=schemas.instalaciones.InstalacionResponse, tags=['Instalacion'], dependencies=[Depends(Portador())])
def create_instalacion(instalacion: schemas.instalaciones.InstalacionCreate, db: Session = Depends(get_db)):
    return crud.instalaciones.create_instalacion(db=db, instalacion=instalacion)

# Actualizar una instalación
@instalacion.put('/instalacion/{id}', response_model=schemas.instalaciones.InstalacionResponse, tags=['Instalacion'], dependencies=[Depends(Portador())])
def update_instalacion(id: int, instalacion: schemas.instalaciones.InstalacionUpdate, db: Session = Depends(get_db)):
    updated_instalacion = crud.instalaciones.update_instalacion(db=db, instalacion_id=id, instalacion=instalacion)
    if not updated_instalacion:
        raise HTTPException(status_code=404, detail="Instalación no encontrada, no se pudo actualizar")
    return updated_instalacion

# Eliminar una instalación
@instalacion.delete('/instalacion/{id}', response_model=schemas.instalaciones.InstalacionResponse, tags=['Instalacion'], dependencies=[Depends(Portador())])
def delete_instalacion(id: int, db: Session = Depends(get_db)):
    deleted_instalacion = crud.instalaciones.delete_instalacion(db=db, instalacion_id=id)
    if not deleted_instalacion:
        raise HTTPException(status_code=404, detail="Instalación no encontrada, no se pudo eliminar")
    return deleted_instalacion
