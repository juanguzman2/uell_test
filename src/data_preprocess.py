import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.variables_categoricas = []
        self.variables_numericas = []

    def limpiar_columnas(self):
        self.df.columns = (
            self.df.columns.str.strip()
            .str.replace(' ', '_')
            .str.replace('-', '_')
            .str.replace('__', '_')
            .str.replace('/n', '')
            .str.replace('\n', '')
            .str.lower()
            .str.replace('__', '_')
        )

    def definir_tipos_de_variables(self):
        self.variables_categoricas = self.df.select_dtypes(include=['object']).columns.tolist()
        self.variables_numericas = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    def reemplazar_valores_nulos(self):
        self.df.replace(['N/A', 'nan', 'NAN'], np.nan, inplace=True)

    def binarizar_categoricas(self):
        def binarizar(x):
            if x == 'X':
                return 1
            elif pd.isna(x):
                return 0
            return x

        for col in self.variables_categoricas:
            self.df[col] = self.df[col].map(binarizar)

    def eliminar_duplicados_y_columnas_vacias(self):
        print(f"Duplicados encontrados: {self.df.duplicated().sum()}")
        self.df = self.df.drop_duplicates()
        self.df = self.df.dropna(thresh=len(self.df) * 0.9, axis=1)

    def transformar_columnas(self):
        self.df['incapacidad_fecha_de_inicio'] = pd.to_datetime(self.df['incapacidad_fecha_de_inicio'], errors='coerce')
        self.df['salario_colaborador'] = pd.to_numeric(self.df['salario_colaborador'], errors='coerce')
        self.df['incapacidad_dias'] = pd.to_numeric(self.df['incapacidad_dias'], errors='coerce')

        self.df['fecha_fin_incapacidad'] = self.df['incapacidad_fecha_de_inicio'] + pd.to_timedelta(self.df['incapacidad_dias'], unit='D')
        self.df['costo_total_incapacidad'] = (self.df['salario_colaborador'] / 30) * self.df['incapacidad_dias']

        if 'c.c_colaborador' in self.df.columns:
            self.df['incapacidades_acumuladas_por_colaborador'] = self.df.groupby('c.c_colaborador')['c.c_colaborador'].transform('count')
            self.df['dias_acumulados_por_colaborador'] = self.df.groupby('c.c_colaborador')['incapacidad_dias'].transform('sum')
            self.df['dias_promedio_por_incapacidad_colaborador'] = (
                self.df['dias_acumulados_por_colaborador'] / self.df['incapacidades_acumuladas_por_colaborador']
            )

        self.df['mes'] = self.df['incapacidad_fecha_de_inicio'].dt.month
        self.df['año'] = self.df['incapacidad_fecha_de_inicio'].dt.year

        if 'c.c_colaborador' in self.df.columns:
            self.df['incapacidades_por_mes'] = self.df.groupby(['año', 'mes'])['c.c_colaborador'].transform('count')

    def limpiar(self):
        self.limpiar_columnas()
        self.definir_tipos_de_variables()
        self.reemplazar_valores_nulos()
        self.binarizar_categoricas()
        self.eliminar_duplicados_y_columnas_vacias()
        self.transformar_columnas()
        return self.df
