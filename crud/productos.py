from sqlalchemy.orm import Session
from models.productos import Producto  
from schemas.productos import ProductoCreate, ProductoUpdate  

def get_productos(db: Session, skip: int = 0, limit: int = 10):
    """Obtener una lista de productos con paginación."""
    return db.query(Producto).offset(skip).limit(limit).all()

def get_producto(db: Session, id: int):
    """Obtener un producto por ID."""
    return db.query(Producto).filter(Producto.ID == id).first()

def get_producto_by_cod_barras(db: Session, cod_barras: str):
    """Obtener un producto por código de barras."""
    return db.query(Producto).filter(Producto.Cod_barras == cod_barras).first()

def create_producto(db: Session, producto: ProductoCreate):
    """Crear un nuevo producto."""
    # Excluir Fecha_registro y Fecha_actualizacion del diccionario antes de pasar los datos
    producto_data = producto.dict(exclude_unset=True, exclude={"Fecha_registro", "Fecha_actualizacion"})
    
    db_producto = Producto(**producto_data)
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def update_producto(db: Session, id: int, producto: ProductoUpdate):
    """Actualizar un producto existente."""
    db_producto = db.query(Producto).filter(Producto.ID == id).first()
    if db_producto:
        for key, value in producto.dict().items():
            setattr(db_producto, key, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, id: int):
    """Eliminar un producto por ID."""
    db_producto = db.query(Producto).filter(Producto.ID == id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto

