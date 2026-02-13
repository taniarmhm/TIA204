from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "Hola mundo"}

@app.get("/espera")
async def esperar():
    await asyncio.sleep(5)
    return {"mensaje": "Esperó 5 segundos"}
