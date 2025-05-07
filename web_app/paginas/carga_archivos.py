import streamlit as st
import pandas as pd
import sys
import os

# Agregar ruta a la carpeta que contiene data_preprocess.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from data_preprocess import DataCleaner

st.title("📋 Uell - Análisis de Incapacidades Médicas")
st.markdown("Sube un archivo Excel o usa el archivo precargado del sistema.")

# Ruta del archivo precargado
default_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw/Incapacidades_Empresa.xlsx'))

uploaded_file = st.file_uploader("Selecciona el archivo Excel (.xlsx)", type=["xlsx"])

# Cargar archivo: del usuario o el por defecto
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    origen = "📤 Archivo subido por el usuario"
else:
    df = pd.read_excel(default_file_path)
    origen = "📂 Archivo base precargado desde el sistema"

# ✅ Aplicar limpieza
cleaner = DataCleaner(df)
df_limpio = cleaner.limpiar()

# Guardar limpio en session_state
st.session_state["df_incapacidades"] = df_limpio

st.success(f"Archivo cargado y limpiado correctamente. Origen: {origen}")
st.subheader("Vista previa del DataFrame limpio")
st.dataframe(df_limpio.head())
