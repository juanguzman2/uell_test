from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
import pandas as pd

from src.predict import predecir  # asegúrate de que esta función no guarda CSV si no se le pide


# === INICIALIZACIÓN FASTAPI ===
app = FastAPI(
    title="API de Predicción de Certificados Médicos",
    description="Sube un archivo Excel (.xlsx) para predecir alertas de certificados inválidos.",
    version="1.0"
)

@app.post("/predecir")
async def predecir_archivo(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="El archivo debe tener extensión .xlsx")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Ejecutar predicción y obtener DataFrame
        df_resultado: pd.DataFrame = predecir(
            path_entrada=tmp_path,
            guardar_csv=False  # no guardar archivo
        )

        os.remove(tmp_path)

        # Convertir DataFrame a JSON para respuesta
        return JSONResponse(content=df_resultado.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")
