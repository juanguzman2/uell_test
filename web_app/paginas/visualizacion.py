import streamlit as st
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
import sys
import os

# Ruta para importar módulos desde src/
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
if src_path not in sys.path:
    sys.path.append(src_path)

import data_eda
from data_preprocess import DataCleaner

# Cargar datos
if "df_incapacidades" not in st.session_state:
    df = pd.read_excel("../data/raw/Incapacidades_Empresa.xlsx")
    st.session_state["df_incapacidades"] = df
else:
    df = st.session_state["df_incapacidades"]

# Limpiar datos
cleaner = DataCleaner(df)
df = cleaner.limpiar()

# Extraer variables
cantidad_incapacidades, colaboradores, costo_total = data_eda.info_general(df)
(
    año_actual, mes_actual, año_anterior, mes_anterior,
    colaboradores_actual, colaboradores_anterior, variacion_colaboradores,
    incapacidades_actual, incapacidades_anterior, variacion_incapacidades,
    costo_total_actual, costo_total_anterior, variacion_costo_total
) = data_eda.obtener_metricas_comparativas_mensuales(df)

df_top_diag, fig_pie_diag, fig_bar_diag = data_eda.obtener_diagnosticos_y_graficas(df)
historico_dias_completo, fig_line = data_eda.obtener_historico_dias_y_grafica(df)
historico_costo_completo, fig_bar = data_eda.obtener_historico_costo_y_grafica(df)



# Sección 1 - Resumen Ejecutivo
with st.container(border=True):
    st.header("🔍 Panorama General de Incapacidades")
    st.markdown("Resumen de incapacidades registradas en la empresa durante el periodo evaluado.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Incapacidades", cantidad_incapacidades)
    c2.metric("Total de Colaboradores", colaboradores)
    c3.metric("Costo Total", f"${costo_total:,.0f}")
    style_metric_cards(background_color="#F0F2F6")

    with st.text("📌 Interpretación Ejecutiva"):
        st.markdown(f"""
        - **Total de Incapacidades Registradas:** Se reportaron **{cantidad_incapacidades} eventos de incapacidad**, indicando una carga significativa de ausentismo.
        - **Total de Colaboradores Afectados:** **{colaboradores} colaboradores** han tenido al menos una incapacidad, lo que sugiere que cerca de 1 de cada 3 empleados se ha visto afectado.
        - **Costo Total Estimado:** Las incapacidades representaron un gasto de más de **${costo_total:,.0f} millones**, lo que resalta una oportunidad clara de ahorro e intervención.

        """)

# Sección 2 - Tendencias Recientes
with st.container(border=True):
    st.header("📅 Comparativo Último Mes")
    st.markdown("Comparación entre el mes actual y el mes anterior en colaboradores, incapacidades y costos.")

    c1, c2, c3 = st.columns(3)
    c2.metric("Total de Colaboradores", colaboradores_actual, delta=variacion_colaboradores)
    c1.metric("Total de Incapacidades", incapacidades_actual, delta=variacion_incapacidades)
    c3.metric("Costo Total", f"${costo_total_actual:,.0f}", delta=variacion_costo_total)

    st.caption(f"🕒 Mes {mes_actual} año {año_actual} vs mes {mes_anterior} año {año_anterior}")

    with st.text("📌 Interpretación Ejecutiva"):
        st.markdown(f"""
        - **Disminución significativa en incapacidades:** Se reportaron **{incapacidades_actual} incapacidades** en el mes actual, **{variacion_incapacidades}% menos** que el mes anterior.
        - **Menos colaboradores afectados:** La cantidad de colaboradores con incapacidades fue **{colaboradores_actual}**, representando una **caída de {variacion_colaboradores}%** frente al mes previo.
        - **Reducción del costo total:** El costo asociado a incapacidades bajó a **${costo_total_actual:,.0f}**, una **disminución del {variacion_costo_total}%** respecto al mes anterior.
       """)
        
# Sección 3 - Diagnósticos Principales
st.header("🧾 Diagnósticos Frecuentes y Críticos")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("Top 10 diagnósticos más comunes:")
    st.dataframe(df_top_diag.head(10), use_container_width=True)

with col2:
    st.plotly_chart(fig_pie_diag, use_container_width=True)

with col3:
    st.plotly_chart(fig_bar_diag, use_container_width=True)

with st.text("📌 Interpretación Ejecutiva"):
    st.markdown(f"""
    ### 🧠 Principales Hallazgos:
    - **Diagnóstico más común:** {df_top_diag.sort_values(by='cantidad_incapacidades',ascending=False).iloc[0,0]} con un total de {df_top_diag.sort_values(by='cantidad_incapacidades',ascending=False).iloc[0,1]} casos, asociado típicamente a infecciones respiratorias.
    - **Mayor cantidad de días ausentes:** {df_top_diag.sort_values(by='dias_ausentes',ascending=False).iloc[0,0]} con un total de {df_top_diag.sort_values(by='dias_ausentes',ascending=False).iloc[0,2]} dias de ausentismo, seguido de {df_top_diag.sort_values(by='dias_ausentes',ascending=False).iloc[1,0]} con un total de {df_top_diag.sort_values(by='dias_ausentes',ascending=False).iloc[1,2]} dias de ausentismo.
    - **Diagnóstico con mayor impacto económico:** {df_top_diag.sort_values(by='costo_diagnostico',ascending=False).iloc[0,0]}, con un costo de {df_top_diag.sort_values(by='costo_diagnostico',ascending=False).iloc[0,-1]}), seguido por {df_top_diag.sort_values(by='costo_diagnostico',ascending=False).iloc[1,0]} y {df_top_diag.sort_values(by='costo_diagnostico',ascending=False).iloc[2,0]}.
    """)

# Sección 4 - Evolución de Días Perdidos
st.header("📊 Histórico de Días Perdidos")
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("Días perdidos por periodo:")
    st.dataframe(historico_dias_completo.sort_values(by='dias_perdidos', ascending=False), use_container_width=True)

with col2:
    st.plotly_chart(fig_line, use_container_width=True)

with st.text("📌 Interpretación Ejecutiva"):
    top_dias = historico_dias_completo.sort_values(by='dias_perdidos', ascending=False).head(1).iloc[0]
    año_max = top_dias['año']
    mes_max = top_dias['mes']
    dias_max = top_dias['dias_perdidos']

    promedio_anual = historico_dias_completo.groupby('año')['dias_perdidos'].sum().mean()
    tendencia_reciente = historico_dias_completo.tail(6)['dias_perdidos'].mean()

    st.markdown(f"""
    ### 🧠 Principales Hallazgos:
    - **Máximo histórico de días perdidos:** Se registraron **{dias_max} días perdidos** en {mes_max} de {año_max}.
    - **Promedio anual de días perdidos:** El promedio anual de días perdidos es de **{promedio_anual:.0f} días**.
    - **Promedio mensual de días perdidos:** El promedio mensual de días perdidos es de **{historico_dias_completo['dias_perdidos'].mean():.0f} días**.

    - **Tendencia reciente:** El promedio de los últimos 6 meses ha sido de **{tendencia_reciente:.0f} días perdidos por mes**, lo cual se mantiene **{'por encima' if tendencia_reciente > promedio_anual else 'por debajo'}** del promedio histórico anual (**{promedio_anual:.0f} días**).
    """)

# Sección 5 - Impacto Económico del Ausentismo
st.header("💵 Periodos con Mayor Costo")
col1, col2 = st.columns([1, 2])

with col1:
    resumen_costo = historico_costo_completo.groupby(['año', 'mes']).sum().sort_values(by='costo_total', ascending=False)
    resumen_costo_reset = resumen_costo.reset_index()  # << Importante para acceder a 'año' y 'mes' como columnas
    st.dataframe(resumen_costo_reset, use_container_width=True)

with col2:
    st.plotly_chart(fig_bar, use_container_width=True)

with st.text("📌 Interpretación Ejecutiva"):
    # Periodo más costoso
    periodo_top = resumen_costo_reset.iloc[0]
    año_top = periodo_top['año']
    mes_top = periodo_top['mes']
    costo_top = periodo_top['costo_total']

    # Promedio últimos 6 meses
    resumen_costo_reset['fecha'] = pd.to_datetime(resumen_costo_reset['año'].astype(str) + "-" + resumen_costo_reset['mes'].astype(str))
    resumen_costo_ordenado = resumen_costo_reset.sort_values(by='fecha')
    promedio_reciente = resumen_costo_ordenado.tail(6)['costo_total'].mean()

    st.markdown(f"""
    ### 🧠 Principales Hallazgos:
    - **Periodo con mayor impacto económico:** {mes_top} {año_top} con un costo total de **${costo_top:,.0f}**.
    - **Promedio de costos anuales:** El promedio anual de costos es de **${resumen_costo_reset['costo_total'].mean():,.0f}**.
    - **Promedio de costos mensuales:** El promedio mensual de costos es de **${resumen_costo_reset['costo_total'].mean():,.0f}**.
   """)