from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
import pandas as pd

from src.predict import predecir  # Asegúrate de que esta función puede aceptar CSV

# === INICIALIZACIÓN FASTAPI ===
app = FastAPI(
    title="API de Predicción de Certificados Médicos",
    description="Sube un archivo Excel (.xlsx) o CSV (.csv) para predecir alertas de certificados inválidos.",
    version="1.1"
)

@app.post("/predecir")
async def predecir_archivo(file: UploadFile = File(...)):
    # Validar tipo de archivo permitido
    if not (file.filename.endswith(".xlsx") or file.filename.endswith(".csv")):
        raise HTTPException(status_code=400, detail="El archivo debe ser .xlsx o .csv")

    # Detectar extensión
    suffix = ".xlsx" if file.filename.endswith(".xlsx") else ".csv"

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Llamada a función de predicción
        df_resultado: pd.DataFrame = predecir(
            path_entrada=tmp_path,
            guardar_csv=False
        )

        os.remove(tmp_path)

        # Respuesta en formato JSON
        return JSONResponse(content=df_resultado.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")
