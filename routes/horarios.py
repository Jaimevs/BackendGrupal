from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import crud.horarios
import config.db
import schemas.horarios
from portadortoken import Portador
from models.horarios import TbbHorarios, Base  # Se asume que el modelo TbbHorarios y su Base existen en models.horarios

horario = APIRouter()
Base.metadata.create_all(bind=config.db.engine)
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta protegida que requiere autenticación JWT mediante Portador
@horario.post("/horarios/", response_model=schemas.horarios.TbbHorariosCreate,tags=["Horarios"], dependencies=[Depends(Portador())])
def crear_horario(
    horario: schemas.horarios.TbbHorariosCreate, 
    db: Session = Depends(get_db),
    usuario: dict = Depends(Portador())  # Obtiene el usuario autenticado
):
    """
    Endpoint para crear un nuevo horario en la base de datos.
    Requiere autenticación JWT.
    """
    try:
        return crud.horarios.create_horario(db=db, horario=horario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@horario.get("/horarios/",tags=["Horarios"], dependencies=[Depends(Portador())])
def obtener_horarios(
    db: Session = Depends(get_db),
    usuario: dict = Depends(Portador())  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para obtener todos los horarios de la base de datos.
    Requiere autenticación JWT.
    """
    try:
        return crud.horarios.All_horarios(db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@horario.put("/horarios/{horario_id}", response_model=schemas.horarios.TbbHorariosCreate,tags=["Horarios"], dependencies=[Depends(Portador())])
def actualizar_horario(
    horario_id: int,
    horario_data: schemas.horarios.TbbHorariosCreate,
    db: Session = Depends(get_db),
    usuario: dict = Depends(Portador())  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para actualizar un horario existente.
    Requiere autenticación JWT.
    """
    try:
        return crud.horarios.update_horario(db=db, horario_id=horario_id, horario_data=horario_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@horario.delete("/horarios/{horario_id}",tags=["Horarios"], dependencies=[Depends(Portador())])
def eliminar_horario(
    horario_id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(Portador())  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para eliminar un horario existente.
    Requiere autenticación JWT.
    """
    try:
        return crud.horarios.delete_horario(db=db, horario_id=horario_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@horario.get("/horarios/{horario_id}", response_model=schemas.horarios.TbbHorariosCreate,tags=["Horarios"], dependencies=[Depends(Portador())])
def obtener_horario_por_id(
    horario_id: int,
    db: Session = Depends(get_db),
    usuario: dict = Depends(Portador())  # Verifica que el usuario esté autenticado
):
    """
    Endpoint protegido para obtener un horario por su ID.
    Requiere autenticación JWT.
    """
    horario = crud.horarios.get_horario_by_id(db, horario_id)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario
