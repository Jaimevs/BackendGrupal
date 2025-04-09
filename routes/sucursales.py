from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models.sucursalesModels
from config.db import get_db
from schemas.sucursalSchemas import SucursalCreate, SucursalUpdate
from schemas.sucursalSchemas import Sucursal as SucursalResponse
from schemas.sucursalSchemas import SucursalResponseGerente
import crud.sucursalesCrud as crud

sucursal = APIRouter(prefix="/sucursales", tags=["Sucursales"])

@sucursal.get("/", response_model=List[SucursalResponseGerente])
def read_sucursales(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_sucursales(db, skip, limit)

# Obtener una sucursal por ID
@sucursal.get("/{id}", response_model=SucursalResponse)
def read_sucursal(id: int, db: Session = Depends(get_db)):
    db_sucursal = crud.get_sucursal(db, id=id)
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return db_sucursal

# Crear una nueva sucursal
@sucursal.post("/", response_model=SucursalResponse, status_code=201)
def create_sucursal(sucursal: SucursalCreate, db: Session = Depends(get_db)):
    return crud.create_sucursal(db, sucursal)

# Actualizar una sucursal existente
@sucursal.put("/{id}", response_model=SucursalResponse)
def update_sucursal(id: int, sucursal: SucursalUpdate, db: Session = Depends(get_db)):
    db_sucursal = crud.update_sucursal(db, id, sucursal)
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return db_sucursal

# "Eliminar" una sucursal (soft delete)
@sucursal.delete("/{id}")
def delete_sucursal(id: int, db: Session = Depends(get_db)):
    result = crud.delete_sucursal(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return result
