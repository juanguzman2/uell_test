import streamlit as st

st.title("🧾 Validación Inteligente de Certificados Médicos")
st.markdown("---")

st.markdown("""
### 🚀 Enfoque General

Para validar certificados médicos de forma **automática, eficiente y escalable**, propongo una solución basada en **visión computacional** y **procesamiento de lenguaje natural (NLP)**, completamente orquestada y adaptable tanto en local como en la nube.

---

### 📥 Ingreso del Certificado

Cuando un empleado sube un certificado (foto o PDF):

- El archivo se **almacena de forma segura**, por ejemplo en un bucket S3 cifrado.
- Se asigna un **ID único** para trazabilidad.
- Se aplican **políticas estrictas de acceso** para proteger la privacidad.

---

### 🔧 Preprocesamiento + OCR (Reconocimiento Óptico de Caracteres)

1. Se realiza limpieza visual: brillo, rotación, nitidez.
2. Se aplica un motor OCR como **Tesseract** o **AWS Textract** para extraer el texto.

---

### 🧠 Extracción Inteligente de Información

A partir del texto obtenido:

- Se detecta la **duración de la incapacidad** (ej. “7 días de reposo”).
- Se extrae el **diagnóstico o motivo** usando:
  - **KeyBERT**
  - **Reglas gramaticales**
- Se reconocen **fechas**, **nombre del médico**, **matrícula**.

➡️ Todo se transforma en un **diccionario estructurado**, sin necesidad de listas manuales de enfermedades.

---

### 💸 Optimización de Costos

La solución se adapta al volumen y recursos de cada cliente:

- Para clientes pequeños, se priorizan herramientas **open source** como Tesseract y YOLOv5, ejecutadas en entornos locales o contenedores ligeros.
- Para clientes con alto volumen, se usa procesamiento por lotes y servicios **serverless** como AWS Lambda y Textract, pagando solo por uso.
- Se implementan prácticas como compresión de imágenes y control de ejecuciones para reducir consumo y mejorar eficiencia.

Esto permite una arquitectura flexible y costo-efectiva sin sacrificar rendimiento.
            
---

### 👁️ Validación de la Estructura Visual

Se aplica **visión computacional (YOLO)** para verificar elementos visuales:

- Firma manuscrita ✍️
- Sello institucional 🏥
- Insignia médica ⚕️

Cada uno genera un **puntaje de confianza**. Si falta alguno, se clasifica como sospechoso o inválido.

---

### 🧾 Decisión y Flujo Operativo

Según la evidencia:

- ✅ **Válido**: se registra automáticamente.
- ⚠️ **Sospechoso**: se envía a revisión manual.
- ❌ **Inválido**: se genera alerta para RR.HH.

Además, todo se **registra con logs**, y los modelos pueden aprender con retroalimentación.

---

### 🔁 Ciclo de Vida del Modelo

El sistema cuenta con monitoreo de rendimiento y data drift, y permite reentrenamiento con nuevos ejemplos etiquetados. Todo el pipeline se gestiona con MLflow y puede desplegarse automáticamente con CI/CD en GitHub Actions.

---

### ☁️ Escalabilidad y Privacidad

- Puede ejecutarse **100% en local** por políticas de privacidad.
- En la nube, se escala con:
  - **Docker**
  - **Kubernetes / AWS Fargate**
- Arquitectura **modular y versionada en Git**.

---

### 🧩 Producto para Clientes

La solución se entrega como:

- Un **microservicio** integrable al portal de RR.HH.
- O vía **API REST**
- O una app web sencilla para subir certificados y recibir resultados.
""")