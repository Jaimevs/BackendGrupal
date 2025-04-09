from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.areas import Areas
from schemas.areas import AreaCreate, AreaResponse, AreaUpdate
from crud.areas import create_area, All_areas, update_area, delete_area, get_area_by_id
from database import get_db  # Asegúrate de importar get_db
from datetime import timedelta
from config.jwt import obtener_usuario_actual, ACCESS_TOKEN_EXPIRE_MINUTES  # Importa desde config/jwt.py

router = APIRouter()

#Ruta para registrar un nuevo area protegida por JWT
@router.post("/area/", response_model=AreaResponse)
def registrar_area(
    area: AreaCreate, 
    db: Session = Depends(get_db), 
    usuario_actual: Areas = Depends(obtener_usuario_actual)
):
    """
    Endpoint para registrar un nuevo area."
    """
    # Llamar a la función de la capa CRUD
    db_area = create_area(db, area)
    if not db_area:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El area ya está registrado",
        )
    return db_area

#Endpoint para obtener todos los areas protegido por JWT
@router.get("/area/", response_model=list[AreaResponse])
def obtener_areas(
    db: Session = Depends(get_db), 
    usuario_actual: Areas = Depends(obtener_usuario_actual)
):
    """
    Endpoint para obtener todos los areas.
    """
    # Llamar a la función de la capa CRUD
    areas = All_areas(db)
    return areas

#Ruta para actualizar un area por ID protegido por JWT
@router.put("/area/{area_id}", response_model=AreaResponse)
def actualizar_area(
    area_id: int,
    area_data: AreaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Areas = Depends(obtener_usuario_actual)
):
    """
    Endpoint para actualizar un area existente.
    """
    # Llamar a la función de la capa CRUD
    area_actualizado = update_area(db, area_id, area_data)
    return area_actualizado

#Ruta para eliminar un area protegido por JWT
@router.delete("/area/{area_id}", response_model=AreaResponse)
def eliminar_area(
    area_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Areas = Depends(obtener_usuario_actual)
):
    """
    Endpoint para eliminar un area por su ID.
    """
    # Llamar a la función de la capa CRUD
    area_eliminado = delete_area(db, area_id)
    return area_eliminado

#ruta para obtener un area por ID protegido por JWT
@router.get("/area/{area_id}", response_model=AreaResponse)
def obtener_area_por_id(
    area_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Areas = Depends(obtener_usuario_actual)
):
    """
    Endpoint para obtener un area por su ID.
    """
    # Llamar a la función de la capa CRUD
    area = get_area_by_id(db, area_id)
    return area