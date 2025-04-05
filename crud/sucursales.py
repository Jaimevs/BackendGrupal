import models.sucursales
import schemas.sucursales
from sqlalchemy.orm import Session
import models, schemas

# Busqueda por id
def get_sucursal(db:Session, id: int):
    return db.query(models.sucursales.Sucursal).filter(models.sucursales.Sucursal.Id == id).first()

# Busqueda por sucursal
def get_sucursal_by_sucursal(db:Session, sucursal: str):
    return db.query(models.sucursales.Sucursal).filter(models.sucursales.Sucursal.Nombre == sucursal).first()

# Buscar todas las sucursales
def get_sucursales(db:Session, skip: int=0, limit:int=10):
    return db.query(models.sucursales.Sucursal).offset(skip).limit(limit).all()

# Crear nueva sucursal
def create_sucursal(db:Session, sucursal: schemas.sucursales.SucursalCreate):
    db_sucursal = models.sucursales.Sucursal(Nombre=sucursal.Nombre,
                                             Direccion=sucursal.Direccion,
                                             Responsable_Id=sucursal.Responsable_Id,
                                             Total_Clientes_Atendidos=sucursal.Total_Clientes_Atendidos,
                                             Promedio_Clientes_X_Dia=sucursal.Promedio_Clientes_X_Dia,
                                             Capacidad_Maxima=sucursal.Capacidad_Maxima,
                                             Total_Empleados=sucursal.Total_Empleados,
                                             Horario_Disponibilidad= sucursal.Horario_Disponibilidad,
                                             Estatus=sucursal.Estatus,
                                             Fecha_Registro=sucursal.Fecha_Registro,
                                             Fecha_Actualizacion=sucursal.Fecha_Actualizacion)
    
    
    db.add(db_sucursal)
    db.commit()
    db.refresh(db_sucursal)
    print(db_sucursal)
    return db_sucursal

# Actualizar una sucursal por id
def update_sucursal(db:Session, id:int, sucursal:schemas.sucursales.SucursalUpdate):
    db_sucursal = db.query(models.sucursales.Sucursal).filter(models.sucursales.Sucursal.Id == id).first()
    if db_sucursal:
        for var, value in vars(sucursal).items():
            setattr(db_sucursal, var, value) if value else None
        db.commit()
        db.refresh(db_sucursal)
    return db_sucursal

# Eliminar una sucursal por id
def delete_sucursal(db:Session, id:int):
    db_sucursal = db.query(models.sucursales.Sucursal).filter(models.sucursales.Sucursal.Id == id).first()
    if db_sucursal:
        db.delete(db_sucursal)
        db.commit()
    return db_sucursal