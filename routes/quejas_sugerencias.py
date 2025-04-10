from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db
import schemas.quejas_sugerencias
import crud.quejas_sugerencias
from portadortoken import Portador
from models.quejas_sugerencias import QuejasSugerencias, Base 

quejasrouter = APIRouter()
Base.metadata.create_all(bind=config.db.engine)
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta protegida para crear una nueva queja o sugerencia
@quejasrouter.post(
    "/quejas_sugerencias/",
    response_model=schemas.quejas_sugerencias.QuejasSugerenciasResponse,
    tags=["Quejas y Sugerencias"],
    dependencies=[Depends(Portador())]
)
def crear_quejas_sugerencias(
    quejas_sugerencias: schemas.quejas_sugerencias.QuejasSugerenciasCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint protegido para crear una nueva queja o sugerencia.
    Requiere autenticación JWT.
    """
    try:
        return crud.quejas_sugerencias.create_quejas_sugerencias(db=db, quejas_sugerencias=quejas_sugerencias)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 

# Ruta protegida para actualizar una queja o sugerencia existente
@quejasrouter.put(
    "/quejas_sugerencias/{queja_id}",
    response_model=schemas.quejas_sugerencias.QuejasSugerenciasResponse,
    tags=["Quejas y Sugerencias"],
    dependencies=[Depends(Portador())]
)
def actualizar_queja_sugerencia(
    queja_id: int,
    queja_data: schemas.quejas_sugerencias.QuejasSugerenciasUpdate,
    db: Session = Depends(get_db)
):
    """
    Endpoint protegido para actualizar una queja o sugerencia existente.
    Requiere autenticación JWT.
    """
    try:
        return crud.quejas_sugerencias.update_queja_sugerencia(
            db=db, queja_sugerencia_id=queja_id, queja_sugerencia_data=queja_data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint protegido para obtener todas las quejas y sugerencias
@quejasrouter.get(
    "/quejas_sugerencias/",
    response_model=list[schemas.quejas_sugerencias.QuejasSugerenciasResponse],
    tags=["Quejas y Sugerencias"],
    dependencies=[Depends(Portador())]
)
def obtener_quejas_sugerencias(
    db: Session = Depends(get_db)
):
    """
    Endpoint protegido para obtener todas las quejas y sugerencias.
    Requiere autenticación JWT.
    """
    try:
        return crud.quejas_sugerencias.All_quejas_sugerencias(db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Endpoint protegido para obtener una queja o sugerencia por su ID
@quejasrouter.get(
    "/quejas_sugerencias/{queja_id}",
    response_model=schemas.quejas_sugerencias.QuejasSugerenciasResponse,
    tags=["Quejas y Sugerencias"],
    dependencies=[Depends(Portador())]
)
def obtener_queja_sugerencia_por_id(
    queja_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint protegido para obtener una queja o sugerencia por su ID.
    Requiere autenticación JWT.
    """
    try:
        return crud.quejas_sugerencias.get_queja_sugerencia_by_id(db=db, queja_sugerencia_id=queja_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
