from sqlalchemy.orm import Session
from models.areas import Areas
from schemas.areas import AreaCreate, AreaUpdate,AreaResponse
from fastapi import HTTPException, status
from datetime import datetime

# funcion para crear un nuevo area 
def create_area(db: Session, area: AreaCreate):
    nuevo_area = Areas(
        Nombre=area.Nombre,
        Descripcion=area.Descripcion,
        Sucursal_ID=area.Sucursal_ID if area.Sucursal_ID is not None else None,
        Estatus=area.Estatus,
        Fecha_Registro=datetime.now(),  # Establecer la fecha de registro actual
        Fecha_Actualizacion=datetime.now(),  # Establecer la fecha de actualización actual
    )
    db.add(nuevo_area)
    db.commit()
    db.refresh(nuevo_area)
    return nuevo_area

#funcion para obtener todos los areas
def All_areas(db: Session):
    """
    Obtener todos los areas de la base de datos.
    """
    return db.query(Areas).all()

#funcion para actualizar un area
def update_area(db: Session, area_id: int, area_data: AreaUpdate):
    """
    Actualizar un area existente.
    """
    area = db.query(Areas).filter(Areas.ID == area_id).first()
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area no encontrado")

    for key, value in area_data.dict(exclude_unset=True).items():
        setattr(area, key, value)

    area.Fecha_Actualizacion = datetime.now()  # Actualizar la fecha de modificación
    db.commit()
    db.refresh(area)
    return area

#funcion para eliminar un area
def delete_area(db: Session, area_id: int):
    """
    Eliminar un area por su ID.
    """
    area = db.query(Areas).filter(Areas.ID == area_id).first()
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area no encontrado")

    db.delete(area)
    db.commit()
    return area

#funcion para obtener un area por ID
def get_area_by_id(db: Session, area_id: int):
    """
    Obtener un area por su ID.
    """
    area = db.query(Areas).filter(Areas.ID == area_id).first()
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area no encontrado")
    return area