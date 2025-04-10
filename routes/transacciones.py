import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from typing import Optional, List
from crud.transacciones import obtener_usuarios_por_transaccion  # en lugar de obtener_usuarios_por_rol
from config.db import get_db
from fastapi import WebSocket
from asyncio import create_task
from models.transacciones import Transaccion
from models.usersrols import UsuarioRol
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload
from webSocket.websocket import manager
from schemas.transacciones import (
    TransaccionCreate,
    TransaccionUpdate,
    TransaccionResponse,
    TipoTransaccion,
    MetodoPago,
    EstatusTransaccion,
    TransaccionEstadisticas
)
from config.db import get_current_user
from crud.transacciones import (
    crear_transaccion,
    obtener_transaccion,
    obtener_todas_transacciones,
    obtener_usuarios_por_rol
)

# Inicializamos el enrutador de transacciones
transaccion = APIRouter()

@transaccion.websocket("/ws/transacciones")
async def websocket_transacciones(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Se mantiene la conexión abierta esperando datos
    except Exception:
        manager.disconnect(websocket)  # Si algo sale mal, desconectamos al cliente


@transaccion.get("/transacciones/estadisticas", response_model=TransaccionEstadisticas, tags=["Transacciones"])
def get_estadisticas_transacciones(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene estadísticas generales de las transacciones.
    """
    try:
        query = text("SELECT * FROM vw_estadisticas_transacciones")
        result = db.execute(query).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="No hay datos estadísticos disponibles.")

        return {
            "total_ingresos": result[0],
            "total_egresos": result[1],
            "balance_general": result[2],
            "transacciones_totales": result[3]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@transaccion.post("/generar-transacciones/", tags=["Transacciones"])
def generar_transacciones_masivas(
    cantidad: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Genera transacciones ficticias en la base de datos mediante un procedimiento almacenado.
    """
    try:
        db.execute(
            text("CALL sp_genera_transacciones(:cantidad)"),
            {"cantidad": cantidad}
        )
        db.commit()
        return {"message": f"Se generaron {cantidad} transacciones correctamente."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@transaccion.get("/obtener-usuarios-por-transaccion", tags=["Transacciones"])
def obtener_usuarios_por_transaccion_route(
    tipo_transaccion: str = Query(...),
    rol: str = Query(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tipo_transaccion = tipo_transaccion.capitalize()

    if tipo_transaccion not in [t.value for t in TipoTransaccion]:
        raise HTTPException(status_code=400, detail="Tipo de transacción no válido")

    usuarios = obtener_usuarios_por_transaccion(db, tipo_transaccion, rol)

    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios con ese rol para la transacción.")

    return usuarios

@transaccion.post("/register-tra/", response_model=TransaccionResponse, tags=["Transacciones"])
async def registrar_transaccion(
    transaccion_data: TransaccionCreate, 
    db: Session = Depends(get_db)
):
    try:
        # Crear la nueva transacción
        nueva_transaccion = crear_transaccion(db, transaccion_data.model_dump())
        
        # Verifica si la transacción fue creada correctamente
        if not nueva_transaccion:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear la transacción")

        # Obtener la transacción con sus datos asociados (usuario y rol)
        transaccion_con_datos = db.query(Transaccion).options(
            joinedload(Transaccion.usuario_rol)  # Cargar la relación 'usuario_rol'
            .joinedload(UsuarioRol.usuario)  # Cargar la relación 'usuario' de UsuarioRol
            .joinedload(UsuarioRol.rol)     # Cargar la relación 'rol' de UsuarioRol
        ).filter(Transaccion.id == nueva_transaccion.id).one_or_none()

        # Si no se encuentra la transacción, lanzar un error
        if not transaccion_con_datos:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transacción no encontrada")

        # Asignar 'nombre_usuario' y 'rol' de manera segura
        usuario_rol = transaccion_con_datos.usuario_rol
        nombre_usuario = usuario_rol.usuario.nombre if usuario_rol and usuario_rol.usuario else None
        rol = usuario_rol.rol.nombre if usuario_rol and usuario_rol.rol else None

        # Convertir la transacción a un modelo Pydantic (TransaccionResponse)
        transaccion_response = TransaccionResponse.from_orm(transaccion_con_datos)
        transaccion_response.nombre_usuario = nombre_usuario
        transaccion_response.rol = rol

        return transaccion_response

    except HTTPException as e:
        # Capturar y levantar errores específicos de HTTP
        raise e

    except Exception as e:
        # Mejorar la captura del error para ver más detalles
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar transacción: {str(e)}"
        )



@transaccion.get("/obtener-todo", response_model=List[TransaccionResponse], tags=["Transacciones"])
def listar_todas_transacciones(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    skip: int = Query(0, description="Número de registros a saltar"),
    limit: int = Query(100, description="Límite de registros por página", le=200),
    tipo_transaccion: Optional[TipoTransaccion] = Query(None, description="Tipo de transacción (Ingreso/Egreso)"),
    metodo_pago: Optional[MetodoPago] = Query(None, description="Método de pago"),
    estatus: Optional[EstatusTransaccion] = Query(None, description="Estatus de transacción"),
    usuario_id: Optional[int] = Query(None, description="ID de usuario"),
    fecha_inicio: Optional[datetime] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[datetime] = Query(None, description="Fecha fin (YYYY-MM-DD)")
):
    """
    Obtiene todas las transacciones con opciones de filtrado y paginación.
    """
    try:
        print(f"Parámetros recibidos: skip={skip}, tipo_transaccion={tipo_transaccion}, metodo_pago={metodo_pago}, estatus={estatus}, usuario_id={usuario_id}, fecha_inicio={fecha_inicio}, fecha_fin={fecha_fin}")
        transacciones = obtener_todas_transacciones(
            db=db,
            skip=skip,
            tipo_transaccion=tipo_transaccion,
            metodo_pago=metodo_pago,
            estatus=estatus,
            usuario_id=usuario_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        print(f"Transacciones obtenidas: {transacciones}")
        return transacciones
    except Exception as e:
        print(f"Error al obtener transacciones: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener transacciones: {str(e)}"
        )

@transaccion.get("/{transaccion_id}", response_model=TransaccionResponse, tags=["Transacciones"])
def obtener_transaccion(
    transaccion_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene los detalles de una transacción específica.
    """
    db_transaccion = obtener_transaccion(db, transaccion_id)
    if not db_transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    return db_transaccion