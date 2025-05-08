import streamlit as st


st.title("📚 Desarrollo Técnico del Análisis de Incapacidades")
st.markdown("""
Esta sección presenta el resumen técnico del desarrollo de la solución implementada para el análisis automatizado de incapacidades médicas.
""")

st.header("⚙️ Proceso de Ingeniería de Datos")
st.markdown("""
- Se diseñó un módulo de limpieza y transformación de datos en el paquete `src/`.
- Se eliminaron registros incompletos, se estandarizaron formatos de fechas y se calcularon métricas derivadas como duración total y costo estimado.
- Se utilizaron técnicas de codificación de variables categóricas y estandarización numérica mediante **pipelines de `scikit-learn`**.
""")

st.header("📊 Selección de Características y Preprocesamiento")
st.markdown("""
- Se aplicó **reducción de colinealidad** (correlación > 0.9) para eliminar redundancia.
- Se utilizó **regresión Lasso** (`L1`) como técnica de selección automática de variables relevantes.
- Se implementó un sistema automático de detección de **data leakage** validado con F1-score.
""")

st.header("🧠 Entrenamiento y Evaluación de Modelos")
st.markdown("""
Se entrenaron distintos algoritmos de clasificación con validación fuera de tiempo:

- `RandomForestClassifier`
- `XGBoostClassifier`
- `LightGBMClassifier`
- `LogisticRegression`

La métrica principal fue el **F1-score**.
""")

st.header("📦 MLOps y Trazabilidad con MLflow")
st.markdown("""
- Se integró **MLflow** para el tracking automático de experimentos, hiperparámetros y métricas.
- Se registraron los modelos con artefactos versionados.
- Los pipelines y transformaciones se documentaron como parte del flujo reproducible.
""")

st.header("🌐 API REST para Inferencia")
st.markdown("""
- Se construyó una API con **FastAPI** alojada en `app.py` que permite realizar inferencias vía HTTP.
- La API recibe archivos Excel, ejecuta el preprocesamiento y devuelve predicciones sobre la validez del certificado.
- Se desplegó exitosamente en la nube usando **Render**, lista para ser integrada con otras plataformas.
""")

st.header("💻 Interfaz Web con Streamlit")
st.markdown("""
- Se desarrolló una **aplicación web en Streamlit** (`visualizacion.py`) para visualizar el análisis exploratorio y ejecutivo.
- Además, se incluyó un módulo de **predicción automática de certificados médicos inválidos**, conectado con la API REST.
- El diseño fue enfocado en claridad visual, storytelling y generación de valor para usuarios no técnicos.
""")

st.header("🔗 Control de Versiones y Entorno")
st.markdown("""
- Todo el proyecto está gestionado bajo control de versiones en **GitHub**, con ramas y commits trazables. El link al repositorio es: [GitHub](https://github.com/juanguzman2/uell_test).
- Se usó un archivo `Docker-compose.yaml` para facilitar el despliegue reproducible y local de la solución.
- Las dependencias se controlan vía `requirements.txt`, y el entorno está preparado para ejecutar en local o en la nube.
""")

st.header("🚀 Mejoras Propuestas")
st.markdown("""
Este proyecto se puede escalar en los siguientes aspectos:

### 💡 Mejora de Alcance Técnico
- **Integración con plataformas BI**: publicar resultados en dashboards como **Power BI** o **Metabase** vía endpoints o bases de datos conectadas.
- **Escalabilidad en la nube**: migrar orquestación completa a **AWS/GCP** y programar DAGs con **Airflow** para automatización.
- **Bases de datos de mayor escala**: usar **PostgreSQL, BigQuery o Spark** para manejar volúmenes más grandes o en tiempo real.

- **Validación productiva**: incluir métricas de drift, monitoreo en tiempo real y reentrenamiento automático.

""")

st.success("📌 Este análisis fue diseñado como una solución escalable, automatizada y alineada a prácticas modernas de MLOps y ciencia de datos.")
