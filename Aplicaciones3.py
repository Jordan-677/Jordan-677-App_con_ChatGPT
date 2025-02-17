import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder

# Función para llenar datos faltantes
def fill_missing_data(df):
    categorical_cols = df.select_dtypes(include=['object']).columns
    numerical_cols = df.select_dtypes(include=np.number).columns
    df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])
    
    if df[numerical_cols].isna().sum().sum() == 0:
        return df  # Si no hay valores nulos, retornar el dataframe sin cambios
    
    data_for_imputation = df.copy()
    le = LabelEncoder()
    data_for_imputation[categorical_cols] = data_for_imputation[categorical_cols].apply(le.fit_transform)
    
    data_for_fitting = data_for_imputation.dropna()
    
    if not data_for_fitting.empty:
        imputer = KNeighborsRegressor(n_neighbors=5)
        imputer.fit(data_for_fitting.drop(numerical_cols, axis=1), data_for_fitting[numerical_cols])
        rows_with_nan = data_for_imputation[numerical_cols].isna().any(axis=1)
        df.loc[rows_with_nan, numerical_cols] = imputer.predict(
            data_for_imputation.loc[rows_with_nan].drop(numerical_cols, axis=1)
        )
    else:
        df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
    
    return df

# Función para cargar archivo
def cargar_datos(url):
    try:
        df = pd.read_csv(url)
        df = fill_missing_data(df)
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

# Función para mostrar estadísticas generales
def mostrar_estadisticas(df):
    st.subheader("Resumen de datos")
    st.write(df.describe())

# Función para mostrar gráfico de especies con mayor volumen
def grafico_top_especies(df):
    top_especies = df.groupby("ESPECIE")["VOLUMEN M3"].sum().nlargest(10).reset_index()
    fig = px.bar(top_especies, x="ESPECIE", y="VOLUMEN M3", title="Top 10 Especies por Volumen")
    st.plotly_chart(fig)

# Función para mapa de calor por departamento
def mapa_calor_departamentos(df):
    vol_por_dpto = df.groupby("DPTO")["VOLUMEN M3"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(vol_por_dpto.pivot_table(values="VOLUMEN M3", index="DPTO"), cmap="YlGnBu", annot=True)
    st.pyplot(fig)

# Función principal
def main():
    st.title("Análisis de Movilización de Madera en Colombia")
    opciones = ["Selecciona una opción", "Cargar archivo", "Ingresar URL"]
    opcion = st.selectbox("Elige una opción", opciones)
    
    if opcion == "Cargar archivo":
        url = "https://raw.githubusercontent.com/Jordan-677/Jordan-677-App_con_ChatGPT/refs/heads/main/Base_de_datos_relacionada_con_madera_movilizada_proveniente_de_Plantaciones_Forestales_Comerciales_20250217.csv"
        df = cargar_datos(url)
        if df is not None:
            mostrar_estadisticas(df)
            grafico_top_especies(df)
            mapa_calor_departamentos(df)
    elif opcion == "Ingresar URL":
        user_url = st.text_input("Ingresa la URL del archivo CSV:")
        if user_url:
            df = cargar_datos(user_url)
            if df is not None:
                mostrar_estadisticas(df)
                grafico_top_especies(df)
                mapa_calor_departamentos(df)

if __name__ == "__main__":
    main()

