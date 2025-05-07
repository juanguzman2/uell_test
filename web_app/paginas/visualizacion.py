import streamlit as st
import plotly.express as px

st.subheader("Costo por Incapacidad")

# ✅ Verificar si el DataFrame está en session_state
if "df_incapacidades" not in st.session_state:
    st.warning("Por favor, carga primero un archivo en la pestaña 'Carga de Archivos'.")
    st.stop()

df = st.session_state["df_incapacidades"]  # ✅ Recuperar el DataFrame

# Selector de cantidad de colaboradores a mostrar
top_n = st.slider("Cantidad de colaboradores a mostrar", min_value=5, max_value=50, value=10, step=1)

# Selector opcional de colaborador específico
colaborador_especifico = st.selectbox("Filtrar por colaborador (opcional)", options=['Todos'] + sorted(df['c.c_colaborador'].dropna().unique().tolist()))

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
