from fastapi import FastAPI

from routes.person import person
from routes.rol import rol
from routes.user import user
from routes.usersrols import userrol
from routes.servicios import servicios_router
from routes.evaluacion_serv import evaluaciones_serv_router
from routes.promociones import promocion_router
from routes.opinion_cliente import opinion_cliente_router
from routes.membresias import membresia
from routes.servicios_clientes import servicio_cliente
from routes.productos import producto
from routes.equipamiento import equipamiento
from routes.mantenimiento import mantenimiento
from routes.instalaciones import instalacion
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TABLAS CON RELACIÓN 
app.include_router(user)
app.include_router(person)
app.include_router(rol)
app.include_router(userrol)
app.include_router(evaluaciones_serv_router)
app.include_router(promocion_router)
app.include_router(opinion_cliente_router)
app.include_router(membresia)
app.include_router(servicio_cliente)
app.include_router(instalacion)
app.include_router(producto)
app.include_router(equipamiento)
app.include_router(mantenimiento)
app.include_router(servicios_router)
app.include_router(equipamiento)
