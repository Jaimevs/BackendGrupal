from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import config.db
import schemas.colaborador
import crud.colaborador
from models.colaboradores import Colaborador, Base
from portadortoken import Portador

# Crear el router y las tablas asociadas a Colaborador
colaborador = APIRouter()
Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para registrar un nuevo colaborador
@colaborador.post(
    "/colaborador/",
    response_model=schemas.colaborador.ColaboradorResponse,
    tags=["Colaboradores"],
    dependencies=[Depends(Portador())]
)
def registrar_colaborador(
    colaborador: schemas.colaborador.ColaboradorCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para registrar un nuevo colaborador.
    Requiere autenticación JWT.
    """
    db_colaborador = crud.colaborador.crear_colaborador(db, colaborador)
    if not db_colaborador:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    return db_colaborador

# Ruta para obtener todos los colaboradores
@colaborador.get(
    "/colaborador/",
    response_model=list[schemas.colaborador.ColaboradorResponse],
    tags=["Colaboradores"],
    dependencies=[Depends(Portador())]
)
def obtener_colaboradores(
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener todos los colaboradores.
    Requiere autenticación JWT.
    """
    return crud.colaborador.All_colaboradores(db)

# Ruta para actualizar un colaborador por ID
@colaborador.put(
    "/colaborador/{colaborador_id}",
    response_model=schemas.colaborador.ColaboradorResponse,
    tags=["Colaboradores"],
    dependencies=[Depends(Portador())]
)
def actualizar_colaborador(
    colaborador_id: int,
    colaborador_data: schemas.colaborador.ColaboradorUpdate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para actualizar un colaborador existente.
    Requiere autenticación JWT.
    """
    colaborador_actualizado = crud.colaborador.update_colaborador(db, colaborador_id, colaborador_data)
    if not colaborador_actualizado:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return colaborador_actualizado

# Ruta para eliminar un colaborador
@colaborador.delete(
    "/colaborador/{colaborador_id}",
    response_model=schemas.colaborador.ColaboradorResponse,
    tags=["Colaboradores"],
    dependencies=[Depends(Portador())]
)
def eliminar_colaborador(
    colaborador_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para eliminar un colaborador por su ID.
    Requiere autenticación JWT.
    """
    colaborador_eliminado = crud.colaborador.delete_colaborador(db, colaborador_id)
    if not colaborador_eliminado:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return colaborador_eliminado

# Ruta para obtener un colaborador por ID
@colaborador.get(
    "/colaborador/{colaborador_id}",
    response_model=schemas.colaborador.ColaboradorResponse,
    tags=["Colaboradores"],
    dependencies=[Depends(Portador())]
)
def obtener_colaborador_por_id(
    colaborador_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener un colaborador por su ID.
    Requiere autenticación JWT.
    """
    colaborador = crud.colaborador.get_colaborador_by_id(db, colaborador_id)
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return colaborador
