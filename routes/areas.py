from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import crud.areas
import config.db
import schemas.areas
from models.areas import Areas, Base  # Se asume que el modelo Areas y su Base existen en models.areas
from portadortoken import Portador

# Crear el router y las tablas asociadas a Areas
area = APIRouter()
Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para registrar un nuevo área (protegida por JWT)
@area.post("/area/", 
          response_model=schemas.areas.AreaResponse, 
          tags=["Áreas"],
          dependencies=[Depends(Portador())])
def registrar_area(
    area_data: schemas.areas.AreaCreate, 
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(Portador())  # Obtiene el usuario del token
):
    """
    Endpoint para registrar un nuevo área.
    Requiere autenticación JWT válida.
    """
    # Verificar permisos del usuario si es necesario
    # if not usuario_actual.get("es_admin"):
    #     raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    db_area = crud.areas.create_area(db, area_data)
    if not db_area:
        raise HTTPException(status_code=400, detail="El área ya está registrada")
    return db_area

# Ruta para obtener todas las áreas (protegida por JWT utilizando Portador)
@area.get("/area/", response_model=List[schemas.areas.AreaResponse], tags=["Áreas"], dependencies=[Depends(Portador())])
def obtener_areas(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todas las áreas.
    """
    areas = crud.areas.All_areas(db)
    return areas

# Ruta para actualizar un área por su ID (protegida por JWT)
@area.put("/area/{area_id}", response_model=schemas.areas.AreaResponse, tags=["Áreas"], dependencies=[Depends(Portador())])
def actualizar_area(
    area_id: int,
    area_data: schemas.areas.AreaUpdate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para actualizar un área existente.
    """
    area_actualizado = crud.areas.update_area(db, area_id, area_data)
    if not area_actualizado:
        raise HTTPException(status_code=404, detail="El área no existe, no se pudo actualizar")
    return area_actualizado

# Ruta para eliminar un área por su ID (protegida por JWT)
@area.delete("/area/{area_id}", response_model=schemas.areas.AreaResponse, tags=["Áreas"], dependencies=[Depends(Portador())])
def eliminar_area(
    area_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para eliminar un área por su ID.
    """
    area_eliminado = crud.areas.delete_area(db, area_id)
    if not area_eliminado:
        raise HTTPException(status_code=404, detail="El área no existe, no se pudo eliminar")
    return area_eliminado

# Ruta para obtener un área por su ID (protegida por JWT)
@area.get("/area/{area_id}", response_model=schemas.areas.AreaResponse, tags=["Áreas"], dependencies=[Depends(Portador())])
def obtener_area_por_id(
    area_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener un área por su ID.
    """
    area_db = crud.areas.get_area_by_id(db, area_id)
    if not area_db:
        raise HTTPException(status_code=404, detail="El área no existe")
    return area_db
