import streamlit as st
import pandas as pd
import requests
import io

# Configuración inicial
st.title("🧠 Predicción de Certificados Médicos Inválidos")
st.markdown("""
Sube un archivo Excel con certificados de incapacidad para identificar automáticamente aquellos que podrían ser inválidos.  
La predicción se realiza mediante un modelo entrenado previamente.
""")

# Subida de archivo
uploaded_file = st.file_uploader("📤 Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    with st.spinner("🔄 Procesando archivo y consultando API..."):
        try:
            # Envío del archivo a la API FastAPI
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            }
            response = requests.post("http://localhost:8000/predecir", files=files)

            if response.status_code == 200:
                # Procesamiento de respuesta
                data = response.json()
                df_resultado = pd.DataFrame(data)

                st.success("✅ Predicción completada con éxito.")
                st.subheader("📄 Resultados Detallados")
                st.dataframe(df_resultado, use_container_width=True)

                # Excel de resultados para descarga
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df_resultado.to_excel(writer, index=False)
                excel_data = output.getvalue()

                # Sección de análisis
                st.subheader("📊 Análisis de Resultados")
                total = len(df_resultado)
                invalidos = df_resultado[df_resultado["prediccion"] == 1].shape[0]
                validos = df_resultado[df_resultado["prediccion"] == 0].shape[0]
                porcentaje = round((invalidos / total) * 100)

                st.metric("Total de Certificados Procesados", total)
                st.metric("Certificados Inválidos Detectados", invalidos)
                st.metric("Porcentaje de Certificados Inválidos", f"{porcentaje} %")

                # Descarga del Excel generado
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
