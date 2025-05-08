import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel

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


    def tratar_categorias_raras(self, threshold=0.0001):
        """
        Agrupa las categorías en 'otros' si su frecuencia relativa es menor al umbral dado.
        El parámetro threshold puede ser ajustado según se requiera.
        """
        for col in self.variables_categoricas:
            # Asegurarse de trabajar con strings
            self.df[col] = self.df[col].astype(str)
            freq = self.df[col].value_counts(normalize=True)
            rare_categories = freq[freq < threshold].index
            self.df[col] = self.df[col].apply(lambda x: 'otros' if x in rare_categories else x)

    def eliminar_duplicados_y_columnas_vacias(self):
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
        self.tratar_categorias_raras()
        self.eliminar_duplicados_y_columnas_vacias()
        self.transformar_columnas()
        return self.df


class DataPreprocessor:
    def __init__(self, df, target):
        self.df = df.copy()
        self.target = target
        self.X = df.drop(columns=[target])
        self.y = df[[target,'c.c_colaborador']]
        self.selected_features = []

    def procesar(self):
        # Convertir categóricas a string
        cat_cols = self.X.select_dtypes(include=['object']).columns.tolist()
        num_cols = self.X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.X[cat_cols] = self.X[cat_cols].astype(str)
    
        # Pipelines
        num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        cat_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer([
            ('num', num_pipeline, num_cols),
            ('cat', cat_pipeline, cat_cols)
        ])

        # Fit-transform
        X_transformed = preprocessor.fit_transform(self.X)

        # Nombres de columnas
        cat_names = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(cat_cols)
        all_columns = num_cols + list(cat_names)
        X_df = pd.DataFrame(X_transformed.toarray() if hasattr(X_transformed, "toarray") else X_transformed,
                            columns=all_columns, index=self.X.index)
        X_df = X_df.drop(columns=['c.c_colaborador'], errors='ignore')

        # Devuelve dataset final
        final_df = pd.concat([self.y, X_df], axis=1)
        return final_df

    def get_features(self):
        return self.selected_features