from fastapi import FastAPI
from services.bigquery import insertar_datos

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API funcionando"}

@app.post("/guardar")
def guardar(data: dict):
    success, error = insertar_datos(data)

    if success:
        return {"status": "ok"}
    else:
        return {"status": "error", "detail": error}