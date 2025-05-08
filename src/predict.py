import pandas as pd
from joblib import load
import os
import sys

# Agregar src al path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_path not in sys.path:
    sys.path.append(src_path)

from data_preprocess import DataCleaner, DataPreprocessor

def predecir(path_entrada: str, guardar_csv: bool = False, output_path: str = "submission.csv") -> pd.DataFrame:
    """
    Realiza predicciones desde un archivo Excel.

    Args:
        path_entrada (str): Ruta del archivo Excel con datos.
        guardar_csv (bool): Si True, guarda el resultado como archivo CSV.
        output_path (str): Ruta de guardado del archivo de salida (si guardar_csv=True).

    Returns:
        pd.DataFrame: DataFrame con ['c.c_colaborador','prediccion','probabilidad']
    """

    print("[INFO] Leyendo archivo Excel...")
    df_raw = pd.read_excel(path_entrada)
    print(f"[INFO] Tamaño del archivo cargado: {df_raw.shape}")

    print("[INFO] Cargando lista de features...")
    features = pd.read_csv(r'data/processed/features.csv').iloc[:, 0].to_list()
    print(f"[INFO] Número de features cargadas: {len(features)}")

    print("[INFO] Cargando modelo entrenado...")
    model = load(r'model/model.pkl')
    print("[INFO] Modelo cargado con éxito.")

    print("[INFO] Iniciando limpieza de datos...")
    cleaner = DataCleaner(df_raw)
    df_clean = cleaner.limpiar()
    print(f"[INFO] Datos tras limpieza: {df_clean.shape}")

    print("[INFO] Iniciando preprocesamiento...")
    processor = DataPreprocessor(df_clean, target='alerta_certificado_invalido')
    df_ready = processor.procesar()
    print(f"[INFO] Datos tras preprocesamiento: {df_ready.shape}")

    df = df_ready.copy()
    df['alerta_certificado_invalido'] = df['alerta_certificado_invalido'].astype(int)

    print("[INFO] Realizando predicción...")
    df['prediccion'] = model.predict(df[features])
    df['probabilidad'] = model.predict_proba(df[features])[:, 1]

    resultado = df[['c.c_colaborador', 'prediccion', 'probabilidad']]
    print("[INFO] Predicción completada.")
    print(f"[INFO] Resultados: {resultado.shape}")

    if guardar_csv:
        resultado.to_csv(output_path, index=False)
        print(f"[INFO] Resultados guardados en: {output_path}")

    return resultado

