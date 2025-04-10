
from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import crud.productos, config.db, schemas.productos, models.productos
from typing import List
from portadortoken import Portador

key = Fernet.generate_key()
f = Fernet(key)

producto = APIRouter()
models.productos.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para obtener todos los productos
@producto.get('/productos/', response_model=List[schemas.productos.Producto],tags=['productos'], dependencies=[Depends(Portador())])
def read_productos(skip: int=0, limit: int=1000, db: Session=Depends(get_db)):
    db_productos = crud.productos.get_productos(db=db,skip=skip, limit=limit)
    return db_productos

# Ruta para obtener un producto por ID
@producto.post("/producto/{id}", response_model=schemas.productos.Producto, tags=["productos"], dependencies=[Depends(Portador())])
def read_producto(id: int, db: Session = Depends(get_db)):
    db_producto= crud.productos.get_producto(db=db, id=id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="producto not found")
    return db_producto

# Ruta para crear un producto
@producto.post('/productos/', response_model=schemas.productos.Producto,tags=['productos'], dependencies=[Depends(Portador())])
def create_producto(producto: schemas.productos.ProductoCreate, db: Session=Depends(get_db)):
    db_productos = crud.productos.get_producto_by_cod_barras(db,cod_barras=producto.Cod_barras)
    if db_productos:
        raise HTTPException(status_code=400, detail="producto existente intenta nuevamente")
    return crud.productos.create_producto(db=db, producto=producto)

# Ruta para actualizar un producto
@producto.put('/productos/{id}', response_model=schemas.productos.Producto,tags=['productos'], dependencies=[Depends(Portador())])
def update_Producto(id:int,producto: schemas.productos.ProductoUpdate, db: Session=Depends(get_db)):
    db_productos = crud.productos.update_producto(db=db, id=id, producto=producto)
    if db_productos is None:
        raise HTTPException(status_code=404, detail="producto no existe, no se pudo actualizar ")
    return db_productos

# Ruta para eliminar un producto
@producto.delete('/productos/{id}', response_model=schemas.productos.Producto,tags=['productos'], dependencies=[Depends(Portador())])
def delete_producto(id:int, db: Session=Depends(get_db)):
    db_productos = crud.productos.delete_producto(db=db, id=id)
    if db_productos is None:
        raise HTTPException(status_code=404, detail="producto no existe, no se pudo eliminar ")
    return db_productos










