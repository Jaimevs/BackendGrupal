from sqlalchemy.orm import Session
from datetime import datetime
from models.horarios import TbbHorarios  # Tu modelo SQLAlchemy
from schemas.horarios import TbbHorariosCreate

def create_horario(db: Session, horario: TbbHorariosCreate):
    # Crear una nueva instancia de TbbHorarios con los datos de Pydantic
    nuevo_horario = TbbHorarios(
        Tipo=horario.Tipo,
        Hora_Inicio=horario.Hora_Inicio,
        Hora_Fin=horario.Hora_Fin,
        Fecha_Registro=datetime.now(),  # Se establece automáticamente
        Fecha_Actualizacion=datetime.now(),  # Se establece automáticamente
        Estatus=horario.Estatus,  # Valor por defecto

    )

    # Agregar la nueva instancia a la sesión de la base de datos
    db.add(nuevo_horario)
    db.commit()  # Confirmar la transacción
    db.refresh(nuevo_horario)  # Obtener los valores actualizados (como el ID generado automáticamente)

    return nuevo_horario

def All_horarios(db: Session):
    """
    Obtener todos los horarios de la base de datos.
    """
    return db.query(TbbHorarios).all()

def get_horario_by_id(db: Session, horario_id: int):
    """
    Obtener un horario por su ID.
    """
    return db.query(TbbHorarios).filter(TbbHorarios.ID == horario_id).first()

def update_horario(db: Session, horario_id: int, horario_data: TbbHorariosCreate):
    """
    Actualizar un horario existente.
    """
    horario = db.query(TbbHorarios).filter(TbbHorarios.ID == horario_id).first()
    if not horario:
        return None

    for key, value in horario_data.dict(exclude_unset=True).items():
        setattr(horario, key, value)

    horario.Fecha_Actualizacion = datetime.now()  # Actualizar la fecha de modificación
    db.commit()
    db.refresh(horario)
    return horario

def delete_horario(db: Session, horario_id: int):
    """
    Eliminar un horario por su ID.
    """
    horario = db.query(TbbHorarios).filter(TbbHorarios.ID == horario_id).first()
    if not horario:
        return None

    db.delete(horario)
    db.commit()
    return horario

