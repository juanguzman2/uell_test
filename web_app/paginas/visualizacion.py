import streamlit as st
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd

st.subheader("Costo por Incapacidad")

df = st.session_state["df_incapacidades"]  # ✅ Recuperar el DataFrame

with st.container(border=True):
    st.title("Dashboard")

    c1,c2 = st.columns(2) # cada una de estas variables representa una columna en el layout de streamlit
    c1.metric(label="Total de Incapacidades", value=len(df), delta=None, delta_color="normal")
    c2.metric(label="Total de Colaboradores", value=len(df['c.c_colaborador'].unique()), delta=None, delta_color="normal")

col1, col2 = st.columns(2) # cada una de estas variables representa una columna en el layout de streamlit
with col1:
    # mostrar dataframe en tabla de los colaboradores con mayor costo por incapacidad
    st.subheader("Colaboradores con Mayor Costo por Incapacidades")
    st.write("Esta tabla muestra los colaboradores con el mayor costo total por incapacidades.")
    st.dataframe(df[['c.c_colaborador', 'costo_total_incapacidad']].sort_values(by='costo_total_incapacidad', ascending=False).head(10))
with col2:
    # mostrar dataframe en tabla de los colaboradores con menor costo por incapacidad
    st.subheader("Colaboradores con Menor Costo por Incapacidades")
    st.write("Esta tabla muestra los colaboradores con el menor costo total por incapacidades.")
    st.dataframe(df[['c.c_colaborador', 'costo_total_incapacidad']].sort_values(by='costo_total_incapacidad', ascending=True).head(10))

df



# Selector de cantidad de colaboradores a mostrar
top_n = st.number_input(
    "Selecciona la cantidad de colaboradores a mostrar",
    min_value=1,
    max_value=len(df['c.c_colaborador'].unique()),
    value=5,
    step=1,
    help	="Número de colaboradores a mostrar en el gráfico."
)

# Selector opcional de colaborador específico
colaborador_especifico = st.number_input(
    "Selecciona un colaborador específico (opcional)",
    min_value=0,
    max_value=len(df['c.c_colaborador'].unique()) - 1,
    value=None,
    format="%d",
    step=1,
    help="Selecciona un colaborador específico para ver su costo total por incapacidades."
)
if colaborador_especifico is not None:
    colaborador_especifico = df['c.c_colaborador'].unique()[colaborador_especifico]
else:
    colaborador_especifico = 'Todos'

# Lógica del gráfico
if colaborador_especifico != 'Todos':
    data_filtrada = df[df['c.c_colaborador'] == colaborador_especifico]
    top_costes = data_filtrada.groupby('c.c_colaborador')['costo_total_incapacidad'].sum().reset_index()
else:
    top_costes = df.groupby('c.c_colaborador')['costo_total_incapacidad'].sum().nlargest(top_n).reset_index()

# Gráfico interactivo
fig1 = px.bar(
    top_costes,
    x='c.c_colaborador',
    y='costo_total_incapacidad',
    title='Colaboradores con Mayor Costo por Incapacidades',
    labels={'c.c_colaborador': 'Colaborador', 'costo_total_incapacidad': 'Costo Total ($)'},
    color='costo_total_incapacidad',
    color_continuous_scale='Blues'
)

fig1.update_layout(xaxis_title='Colaborador', yaxis_title='Costo Total ($)')
st.plotly_chart(fig1)
