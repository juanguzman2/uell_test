import streamlit as st
import pandas as pd
import requests
import io

# ====== Configuración de la App ======
st.title("🧠 Predicción de Certificados Médicos Inválidos")
st.markdown("""
Sube un archivo Excel o CSV con certificados de incapacidad para identificar automáticamente aquellos que podrían ser inválidos.  
La predicción se realiza mediante un modelo entrenado previamente alojado en una API.
""")

# ====== Input para la URL de la API ======
api_url = "https://uell-test.onrender.com/predecir"

# ====== Subida de archivo ======
uploaded_file = st.file_uploader("📤 Sube tu archivo (.xlsx o .csv)", type=["xlsx", "csv"])

# ====== Procesamiento al subir archivo ======
if uploaded_file:
    with st.spinner("🔄 Procesando archivo y consultando API..."):
        try:
            # Detectar tipo de archivo
            if uploaded_file.name.endswith('.csv'):
                file_type = "text/csv"
            else:
                file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    file_type,
                )
            }

            response = requests.post(api_url, files=files)

            if response.status_code == 200:
                data = response.json()
                if not data:
                    st.warning("⚠️ La API respondió correctamente, pero no se encontraron predicciones.")
                else:
                    df_resultado = pd.DataFrame(data)

                    st.success("✅ Predicción completada con éxito.")
                    st.subheader("📄 Resultados Detallados")
                    st.dataframe(df_resultado, use_container_width=True)

                    # Exportar resultados a Excel
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df_resultado.to_excel(writer, index=False)
                    excel_data = output.getvalue()

                    # Métricas
                    st.subheader("📊 Análisis de Resultados")
                    total = len(df_resultado)
                    invalidos = df_resultado[df_resultado["prediccion"] == 1].shape[0]
                    porcentaje = round((invalidos / total) * 100) if total else 0

                    st.metric("Total de Certificados Procesados", total)
                    st.metric("Certificados Inválidos Detectados", invalidos)
                    st.metric("Porcentaje de Certificados Inválidos", f"{porcentaje} %")

                    # Botón para descargar
                    st.download_button(
                        label="⬇️ Descargar archivo con predicciones",
                        data=excel_data,
                        file_name="predicciones_certificados.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.error(f"❌ Error al procesar el archivo: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"❌ No se pudo conectar con la API: {e}")

            
