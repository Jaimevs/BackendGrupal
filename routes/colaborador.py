from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.colaboradores import Colaborador
from schemas.colaborador import ColaboradorCreate, ColaboradorResponse, ColaboradorUpdate
from crud.colaborador import crear_colaborador, All_colaboradores, update_colaborador, delete_colaborador,get_colaborador_by_id
from database import get_db  # Asegúrate de importar get_db
from datetime import timedelta
from config.jwt import obtener_usuario_actual, ACCESS_TOKEN_EXPIRE_MINUTES  # Importa desde config/jwt.py

router = APIRouter()

#ruta para registrar un nuevo colaborador
@router.post("/colaborador/", response_model=ColaboradorResponse)
def registrar_colaborador(
    colaborador: ColaboradorCreate, 
    db: Session = Depends(get_db), 
    usuario_actual: Colaborador = Depends(obtener_usuario_actual)
):
    """
    Endpoint para registrar un nuevo colaborador."
    """
    # Llamar a la función de la capa CRUD
    db_colaborador = crear_colaborador(db, colaborador)
    if not db_colaborador:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )
    return db_colaborador

#ruta para obtener todos los colaboradores
@router.get("/colaborador/", response_model=list[ColaboradorResponse])
def obtener_colaboradores(
    db: Session = Depends(get_db), 
    usuario_actual: Colaborador = Depends(obtener_usuario_actual)
):
    """
    Endpoint para obtener todos los colaboradores.
    """
    # Llamar a la función de la capa CRUD
    colaboradores = All_colaboradores(db)
    return colaboradores

#ruta para actualizar un colaborador por ID
@router.put("/colaborador/{colaborador_id}", response_model=ColaboradorResponse)
def actualizar_colaborador(
    colaborador_id: int,
    colaborador_data: ColaboradorUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Colaborador = Depends(obtener_usuario_actual)
):
    """
    Endpoint para actualizar un colaborador existente.
    """
    # Llamar a la función de la capa CRUD
    colaborador_actualizado = update_colaborador(db, colaborador_id, colaborador_data)
    return colaborador_actualizado

#ruta para eliminar un colaborador
@router.delete("/colaborador/{colaborador_id}", response_model=ColaboradorResponse)
def eliminar_colaborador(
    colaborador_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Colaborador = Depends(obtener_usuario_actual)
):
    """
    Endpoint para eliminar un colaborador por su ID.
    """
    # Llamar a la función de la capa CRUD
    colaborador_eliminado = delete_colaborador(db, colaborador_id)
    return colaborador_eliminado


#ruta protegida para obtener un colaborador por ID
@router.get("/colaborador/{colaborador_id}", response_model=ColaboradorResponse)
def obtener_colaborador_por_id(
    colaborador_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Colaborador = Depends(obtener_usuario_actual)
):
    """
    Endpoint para obtener un colaborador por su ID.
    """
    # Llamar a la función de la capa CRUD
    colaborador = get_colaborador_by_id(db, colaborador_id)
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return colaborador
