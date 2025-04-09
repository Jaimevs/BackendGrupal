from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.horarios import TbbHorariosCreate, TbbHorarios
from models.usuarios import Usuario  # Tu modelo para usuarios
from crud.horarios import create_horario,All_horarios,update_horario,delete_horario,get_horario_by_id  # La función que creaste para insertar horarios
from config.jwt import obtener_usuario_actual  # Dependencia que verifica al usuario autenticado
from database import get_db

router = APIRouter()

# Ruta protegida que requiere autenticación
@router.post("/horarios/", response_model=TbbHorariosCreate)
def crear_horario(
    horario: TbbHorariosCreate, 
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)  # Verifica que el usuario esté autenticado
):
    """
    Endpoint para crear un nuevo horario en la base de datos.
    Requiere autenticación.
    """
    # Crear un nuevo horario usando la función que hemos definido
    try:
        return create_horario(db=db, horario=horario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/horarios/")
def obtener_horarios(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para obtener todos los horarios de la base de datos.
    Requiere autenticación.
    """
    try:
        return All_horarios(db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/horarios/{horario_id}", response_model=TbbHorariosCreate)
def actualizar_horario(
    horario_id: int,
    horario_data: TbbHorariosCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para actualizar un horario existente.
    Requiere autenticación.
    """
    try:
        return update_horario(db=db, horario_id=horario_id, horario_data=horario_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/horarios/{horario_id}")
def eliminar_horario(
    horario_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para eliminar un horario existente.
    Requiere autenticación.
    """
    try:
        return delete_horario(db=db, horario_id=horario_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/horarios/{horario_id}", response_model=TbbHorariosCreate)
def obtener_horario_por_id(
    horario_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para obtener un horario por su ID.
    Requiere autenticación.
    """
    horario = get_horario_by_id(db, horario_id)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario
