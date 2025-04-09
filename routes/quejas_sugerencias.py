from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.quejas_sugerencias import QuejasSugerenciasCreate,QuejasSugerenciasUpdate,QuejasSugerenciasResponse
from models.usuarios import Usuario
from crud.quejas_sugerencias import All_quejas_sugerencias,update_queja_sugerencia,get_queja_sugerencia_by_id,create_quejas_sugerencias
from config.jwt import obtener_usuario_actual  # Dependencia que verifica al usuario autenticado
from database import get_db

router = APIRouter()

#ruta protegida para crear una nueva queja o sugerencia
@router.post("/quejas_sugerencias/", response_model=QuejasSugerenciasResponse)
def crear_quejas_sugerencias(
    quejas_sugerencias: QuejasSugerenciasCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para crear una nueva queja o sugerencia.
    Requiere autenticación.
    """
    try:
        return create_quejas_sugerencias(db=db, quejas_sugerencias=quejas_sugerencias)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 

# Ruta protegida que requiere autenticación
@router.put("/quejas_sugerencias/{queja_id}", response_model=QuejasSugerenciasCreate)
def actualizar_queja_sugerencia(
    queja_id: int,
    queja_data: QuejasSugerenciasUpdate,  # Asegúrate de usar el esquema correcto
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    """
    Endpoint protegido para actualizar una queja o sugerencia existente.
    Requiere autenticación.
    """
    try:
        return update_queja_sugerencia(db=db, queja_sugerencia_id=queja_id, queja_sugerencia_data=queja_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
#endpoint para obtener todas las quejas y sugerencias
@router.get("/quejas_sugerencias/")
def obtener_quejas_sugerencias(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para obtener todas las quejas y sugerencias de la base de datos.
    Requiere autenticación.
    """
    try:
        return All_quejas_sugerencias(db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
#endpoint para obtener una queja o sugerencia por su id
@router.get("/quejas_sugerencias/{queja_id}", response_model=QuejasSugerenciasCreate)
def obtener_queja_sugerencia_por_id(
    queja_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para obtener una queja o sugerencia por su ID.
    Requiere autenticación.
    """
    try:
        return get_queja_sugerencia_by_id(db=db, queja_sugerencia_id=queja_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))