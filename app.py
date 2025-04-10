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
from routes.expediente_medicoRoutes import router as expediente_router
from routes.dietas import router as dietas_router
from routes.ejercicios import router as ejercicios_router
from routes.indicadores_nutricionales import router as indicadores_router
from routes.objetivo_programa import router as objetivos_router
from routes.programas_saludables import router as programas_router
from routes.rutinas import router as rutinas_router
from routes.sucursales import sucursal
from routes.transacciones import transaccion
from fastapi.middleware.cors import CORSMiddleware

from routes.areas import area  # Ruta para áreas
from routes.horarios import horario # Ruta para horarios
from routes.quejas_sugerencias import quejasrouter  # Ruta para quejas y sugerencias
from routes.colaborador import colaborador


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
app.include_router(area)  # Se incluye la nueva ruta para áreas
app.include_router(horario)  # Se incluye la nueva ruta para horarios
app.include_router(quejasrouter)  # Se incluye la nueva ruta para quejas y sugerencias
app.include_router(colaborador)  # Se incluye la nueva ruta para colaboradores
app.include_router(instalacion)
app.include_router(producto)
app.include_router(equipamiento)
app.include_router(mantenimiento)
app.include_router(servicios_router)
app.include_router(equipamiento)
app.include_router(expediente_router)
app.include_router(dietas_router)
app.include_router(ejercicios_router)
app.include_router(indicadores_router)
app.include_router(objetivos_router)
app.include_router(programas_router)
app.include_router(rutinas_router)
app.include_router(sucursal)
app.include_router(transaccion)