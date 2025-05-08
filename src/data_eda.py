import pandas as pd
import plotly.express as px

def info_general(df: pd.DataFrame):
    cantidad_incapacidades = df.shape[0]
    colaboradores = df['c.c_colaborador'].nunique()
    costo_total = round(df['costo_total_incapacidad'].sum())

    return cantidad_incapacidades, colaboradores, costo_total

def obtener_metricas_comparativas_mensuales(df: pd.DataFrame):
    """
    Retorna métricas individuales del último mes y su comparación con el mes anterior.

    Parámetros:
    df -- DataFrame con columnas: 'año', 'mes', 'c.c_colaborador', 'costo_total_incapacidad'

    Retorna (en orden):
    año_actual, mes_actual,
    año_anterior, mes_anterior,
    colaboradores_actual, colaboradores_anterior, variacion_colaboradores,
    incapacidades_actual, incapacidades_anterior, variacion_incapacidades,
    costo_total_actual, costo_total_anterior, variacion_costo_total
    """
    # Último año y mes
    ultimo_año = df[df['año'] == df['año'].max()]
    año_actual = ultimo_año['año'].max()
    mes_actual = ultimo_año['mes'].max()
    mes_anterior = mes_actual - 1
    año_anterior = año_actual  # Asume mismo año

    # Filtrar meses
    ultimo_mes = ultimo_año[ultimo_año['mes'] == mes_actual]
    anterior_mes_df = ultimo_año[ultimo_año['mes'] == mes_anterior]

    # Colaboradores (número de registros)
    colaboradores_actual = ultimo_mes.shape[0]
    colaboradores_anterior = anterior_mes_df.shape[0]
    variacion_colaboradores = round((colaboradores_actual - colaboradores_anterior) / colaboradores_anterior * 100, 2) if colaboradores_anterior != 0 else None

    # Incapacidades únicas
    incapacidades_actual = ultimo_mes['c.c_colaborador'].nunique()
    incapacidades_anterior = anterior_mes_df['c.c_colaborador'].nunique()
    variacion_incapacidades = round((incapacidades_actual - incapacidades_anterior) / incapacidades_anterior * 100, 2) if incapacidades_anterior != 0 else None

    # Costo total
    costo_total_actual = round(ultimo_mes['costo_total_incapacidad'].sum())
    costo_total_anterior = round(anterior_mes_df['costo_total_incapacidad'].sum())
    variacion_costo_total = round((costo_total_actual - costo_total_anterior) / costo_total_anterior * 100, 2) if costo_total_anterior != 0 else None

    return año_actual, mes_actual,  año_anterior, mes_anterior, colaboradores_actual, colaboradores_anterior, variacion_colaboradores, incapacidades_actual, incapacidades_anterior, variacion_incapacidades, costo_total_actual, costo_total_anterior, variacion_costo_total
    
def obtener_diagnosticos_y_graficas(df: pd.DataFrame):
    """
    Calcula y retorna:
    - Tabla resumen con las columnas: cantidad_incapacidades, dias_ausentes, costo_diagnostico
    - Gráfico de pastel (pie chart) con top 10 diagnósticos por días ausentes
    - Gráfico de barras (bar chart) con top 10 diagnósticos por costo total

    Parámetros:
    df -- DataFrame original con columnas:
          'incapacidad_diagnóstico', 'incapacidad_dias', 'costo_total_incapacidad'

    Retorna:
    - df_top (DataFrame con métricas)
    - fig_pie (plotly.graph_objects.Figure)
    - fig_bar (plotly.graph_objects.Figure)
    """

    # Diagnósticos más frecuentes
    top_10_diagnosticos = (
        df.groupby('incapacidad_diagnóstico')['incapacidad_diagnóstico']
        .count()
        .reset_index(name='cantidad_incapacidades')
        .sort_values(by='cantidad_incapacidades', ascending=False)
    )

    # Días ausentes
    top_10_diagnosticos_dias = (
        df.groupby('incapacidad_diagnóstico')['incapacidad_dias']
        .sum()
        .reset_index(name='dias_ausentes')
    )

    # Costo por diagnóstico
    costo_diagnostico = (
        df.groupby('incapacidad_diagnóstico')['costo_total_incapacidad']
        .sum()
        .reset_index(name='costo_diagnostico')
    )

    # Merge
    df_top = pd.merge(top_10_diagnosticos, top_10_diagnosticos_dias, on='incapacidad_diagnóstico', how='left')
    df_top = pd.merge(df_top, costo_diagnostico, on='incapacidad_diagnóstico', how='left')
    df_top['costo_diagnostico'] = df_top['costo_diagnostico'].round()

    # Pie chart - top 10 por días ausentes
    df_top_pie = df_top.sort_values(by='dias_ausentes', ascending=False).head(10)
    fig_pie = px.pie(
        df_top_pie,
        names='incapacidad_diagnóstico',
        values='dias_ausentes',
        title='Top 10 Diagnósticos con más Días de Incapacidad',
        hole=0.3
    )

    # Bar chart - top 10 por costo
    df_top_bar = df_top.sort_values(by='costo_diagnostico', ascending=False).head(10)
    fig_bar = px.bar(
        df_top_bar,
        x='incapacidad_diagnóstico',
        y='costo_diagnostico',
        title='Top 10 Diagnósticos con Mayor Costo Total',
        labels={'incapacidad_diagnóstico': 'Diagnóstico', 'costo_diagnostico': 'Costo ($)'},
    )
    fig_bar.update_layout(xaxis_tickangle=-45)

    return df_top, fig_pie, fig_bar

def obtener_historico_dias_y_grafica(df: pd.DataFrame):
    """
    Genera una tabla y un gráfico de línea con el histórico mensual de días perdidos por incapacidad.

    Parámetros:
    df -- DataFrame original con columnas: 'año', 'mes', 'incapacidad_dias'

    Retorna:
    - historico_dias_completo (DataFrame con columnas: año, mes, dias_perdidos)
    - fig_line (plotly.graph_objects.Figure con la evolución de días perdidos)
    """

    # Agrupar por año y mes
    historico = (
        df.groupby(['año', 'mes'])['incapacidad_dias']
        .sum()
        .reset_index(name='dias_perdidos')
    )

    # Asegurar formato entero
    historico['año'] = historico['año'].astype(int)
    historico['mes'] = historico['mes'].astype(int)

    # Crear columna de fecha (1er día del mes)
    historico['date'] = pd.to_datetime(historico['año'].astype(str) + '-' + historico['mes'].astype(str) + '-01')

    # Crear rango completo de fechas
    date_range = pd.date_range(start=historico['date'].min(), end=historico['date'].max(), freq='MS')
    df_full = pd.DataFrame({'date': date_range})
    df_full['año'] = df_full['date'].dt.year
    df_full['mes_num'] = df_full['date'].dt.month

    # Unir con los datos originales
    df_full = df_full.merge(
        historico[['año', 'mes', 'dias_perdidos']],
        left_on=['año', 'mes_num'],
        right_on=['año', 'mes'],
        how='left'
    )
    df_full['dias_perdidos'] = df_full['dias_perdidos'].fillna(0)

    # Asignar nombre de mes y ordenar
    df_full['mes'] = df_full['date'].dt.month_name()
    historico_dias_completo = df_full[['año', 'mes', 'dias_perdidos']].copy()

    historico_dias_completo['mes'] = pd.Categorical(
        historico_dias_completo['mes'],
        categories=[
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ],
        ordered=True
    )
    historico_dias_completo = historico_dias_completo.sort_values(by=['año', 'mes'])

    # Gráfico de línea
    fig_line = px.line(
        df_full,
        x='date',
        y='dias_perdidos',
        title='Evolución Mensual de Días Perdidos por Incapacidad',
        labels={'dias_perdidos': 'Días Perdidos', 'date': 'Fecha'},
        markers=True
    )

    return historico_dias_completo, fig_line


def obtener_historico_costo_y_grafica(df: pd.DataFrame):
    """
    Calcula el histórico mensual de costo por incapacidades y genera un gráfico de barras,
    coloreado por nombre del mes.

    Parámetros:
    df -- DataFrame con columnas: 'año', 'mes', 'costo_total_incapacidad'

    Retorna:
    - historico_costo_completo (DataFrame con columnas: año, mes, costo_total)
    - fig_bar (plotly.graph_objects.Figure)
    """

    # Agrupación
    historico_costo = (
        df.groupby(['año', 'mes'])['costo_total_incapacidad']
        .sum()
        .reset_index(name='costo_total')
    )
    historico_costo['año'] = historico_costo['año'].astype(int)
    historico_costo['mes'] = historico_costo['mes'].astype(int)
    historico_costo['date'] = pd.to_datetime(historico_costo['año'].astype(str) + '-' + historico_costo['mes'].astype(str) + '-01')

    # Relleno de fechas faltantes
    date_range = pd.date_range(start=historico_costo['date'].min(), end=historico_costo['date'].max(), freq='MS')
    df_full_cost = pd.DataFrame({'date': date_range})
    df_full_cost['año'] = df_full_cost['date'].dt.year
    df_full_cost['mes_num'] = df_full_cost['date'].dt.month

    df_full_cost = df_full_cost.merge(
        historico_costo[['año', 'mes', 'costo_total']],
        left_on=['año', 'mes_num'],
        right_on=['año', 'mes'],
        how='left'
    )
    df_full_cost['costo_total'] = df_full_cost['costo_total'].fillna(0)

    # Agregar nombre del mes y formato de fecha
    df_full_cost['mes'] = df_full_cost['date'].dt.month_name()
    df_full_cost['label'] = df_full_cost['date'].dt.strftime('%Y-%m')
    df_full_cost['año'] = df_full_cost['año'].astype(str)

    # Ordenar tabla
    historico_costo_completo = df_full_cost[['año', 'mes', 'costo_total']].copy()
    historico_costo_completo['mes'] = pd.Categorical(
        historico_costo_completo['mes'],
        categories=[
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ],
        ordered=True
    )
    historico_costo_completo = historico_costo_completo.sort_values(by=['año', 'mes'])
    historico_costo_completo['costo_total'] = historico_costo_completo['costo_total'].round()

    # 🎨 Gráfico de barras con color por mes
    fig_bar = px.bar(
        df_full_cost,
        x='label',
        y='costo_total',
        color='mes',
        title='Costo Mensual Total por Incapacidades (coloreado por mes)',
        labels={'label': 'Mes-Año', 'costo_total': 'Costo Total ($)', 'mes': 'Mes'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_bar.update_layout(xaxis_tickangle=-45)

    return historico_costo_completo, fig_bar