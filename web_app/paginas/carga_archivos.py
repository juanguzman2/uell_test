import streamlit as st
import pandas as pd
import sys
import os

# Agregar ruta a la carpeta que contiene data_preprocessing.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from data_preprocess import DataCleaner


st.title("📋 Uell - Análisis de Incapacidades Médicas")
st.markdown("Sube un archivo Excel para cargarlo al sistema.")

uploaded_file = st.file_uploader("Selecciona el archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ✅ Aplicar limpieza
    cleaner = DataCleaner(df)
    df_limpio = cleaner.limpiar()

    # Guardar limpio en session_state
    st.session_state["df_incapacidades"] = df_limpio

    st.success("Archivo cargado y limpiado correctamente. Puedes navegar a las otras páginas.")
    st.subheader("Vista previa del DataFrame limpio")
    st.dataframe(df_limpio.head())
