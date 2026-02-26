from fastapi import FastAPI, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI(
    title="Mi primer API",
    description="Tania Mejia",
    version="1.0"
)

# TABLA FICTICIA
usuarios = [
    {"id": 1, "nombre": "Diego", "edad": 21},
    {"id": 2, "nombre": "Coral", "edad": 21},
    {"id": 3, "nombre": "Saúl", "edad": 21},
    {"id": 4, "nombre": "María", "edad": 21}
]




#################################
# modelo Pydantic de validación #
#################################
class crear_Usuario(BaseModel):
    id: int= Field(..., gt=0,description="identificador de usuario")
 
    nombre: str=Field(...,min_legth = 3, max_length=50, example="Pepe")
    edad: int = Field (..., get=1, le=125,description="edad valida entre 1 y 125")

    



# -------- GET INICIO --------
@app.get("/")
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI"}

# -------- GET UNO --------
@app.get("/v1/usuario/{id}")
async def consultauno(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            return usuario

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# -------- GET TODOS --------
@app.get("/v1/usuarios/")
async def consultatodos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return usuario
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "total": len(usuarios),
        "usuarios": usuarios
    }
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- POST --------
@app.post("/v1/usuarios/")
async def agregar_usuario(nuevo_usuario: dict):

    for usuario in usuarios:
        if usuario["id"] == nuevo_usuario["id"]:
            raise HTTPException(
                status_code=400,
                detail="El ID ya existe"
            )

    usuarios.append(nuevo_usuario)

    return {
        "mensaje": "Usuario agregado correctamente",
        "usuario": nuevo_usuario
    }

# -------- PUT --------
@app.put("/v1/usuario/{id}")
async def actualizar_usuario(id: int, datos: dict):

    for usuario in usuarios:
        if usuario["id"] == id:
            usuario.update(datos)
            return {
                "mensaje": "Usuario actualizado correctamente",
                "usuario": usuario
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# -------- DELETE --------
@app.delete("/v1/usuario/{id}") 
async def eliminar_usuario(id: int):

    for i, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            eliminado = usuarios.pop(i)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "usuario": eliminado
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#