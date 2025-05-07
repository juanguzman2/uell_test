import streamlit as st


st.set_page_config(layout="wide", page_title="Curso streamlit", page_icon="😎")

st.title("Entrgeable uell - Análisis de Incapacidades Médicas")

st.sidebar.success("Menú de navegación")

pages = {
    "Carga de archivos": [
        st.Page("paginas/carga_archivos.py", title="Carga de archivos", icon="📤"),
                ],
    "Análisis de datos": [
        st.Page("paginas/visualizacion.py", title="Análisis de datos", icon="📊"),
                ]

    }

pg = st.navigation(pages,position="sidebar")
pg.run()