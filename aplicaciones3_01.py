import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from scipy.stats import entropy

# Función para llenar datos faltantes con explicaciones detalladas
def fill_missing_data(df):
    """Llenar datos faltantes utilizando diferentes estrategias:
    - Para columnas categóricas: Se reemplazan con la moda (valor más frecuente).
    - Para columnas numéricas:
      - Si hay suficientes datos, se usa la interpolación lineal.
      - Si hay muchos valores nulos, se usa la mediana.
    """
    categorical_cols = df.select_dtypes(include=['object']).columns
    numerical_cols = df.select_dtypes(include=np.number).columns
    
    # Rellenar valores categóricos con la moda
    df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])
    
    # Manejo de valores numéricos
    for col in numerical_cols:
        if df[col].isna().sum() > 0:
            if df[col].isna().sum() / len(df) < 0.1:  # Si hay menos del 10% de valores nulos
                df[col] = df[col].interpolate(method='linear')
            else:
                df[col] = df[col].fillna(df[col].median())
    
    return df

# Función para cargar datos
def cargar_datos(url):
    try:
        df = pd.read_csv(url)
        df = fill_missing_data(df)
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

# Funcionalidad 1: Identificar los puestos de trabajo más comunes y su distribución
def distribucion_puestos(df):
    st.subheader("Distribución de los Puestos de Trabajo por Tipo de Compañía")
    fig = px.histogram(df, x="relevent_experience", color="company_type", barmode="group",
                       title="Puestos de Trabajo y Tipo de Compañía")
    st.plotly_chart(fig)

# Funcionalidad 2: Mapa de ubicación de los candidatos
def mapa_ciudades(df):
    st.subheader("Mapa de Ubicación de los Candidatos")
    fig = px.scatter_geo(df, locations="city", locationmode='country names',
                         title="Ubicación Geográfica de los Candidatos")
    st.plotly_chart(fig)

# Funcionalidad 3: Niveles de educación totales y por género
def educacion_por_genero(df):
    st.subheader("Niveles de Educación Totales y por Género")
    fig1 = px.histogram(df, x="education_level", title="Distribución General de los Niveles Educativos")
    st.plotly_chart(fig1)
    fig2 = px.histogram(df, x="education_level", color="gender", barmode="group",
                         title="Distribución de Niveles Educativos por Género")
    st.plotly_chart(fig2)

# Funcionalidad 4: Características de las industrias
def industrias_ciencia_datos(df):
    st.subheader("Análisis de las Industrias en Ciencia de Datos")
    fig = px.bar(df, x="company_type", y="company_size", title="Características de las Industrias")
    st.plotly_chart(fig)

# Funcionalidad 5: Clustering de ofertas de trabajo
def clustering_ofertas(df):
    st.subheader("Clustering de Ofertas de Trabajo")
    df_cluster = df[['city_development_index', 'training_hours']].dropna()
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_cluster)
    kmeans = KMeans(n_clusters=4, random_state=42)
    df_cluster['Cluster'] = kmeans.fit_predict(df_scaled)
    fig = px.scatter(df_cluster, x='city_development_index', y='training_hours', color='Cluster',
                     title='Segmentación de Ofertas de Trabajo')
    st.plotly_chart(fig)

# Funcionalidad 6: Clustering de candidatos
def clustering_candidatos(df):
    st.subheader("Clustering de Candidatos")
    df_cluster = df[['city_development_index', 'experience']].dropna()
    df_cluster['experience'] = pd.to_numeric(df_cluster['experience'], errors='coerce')
    df_cluster.dropna(inplace=True)
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_cluster)
    kmeans = KMeans(n_clusters=4, random_state=42)
    df_cluster['Cluster'] = kmeans.fit_predict(df_scaled)
    fig = px.scatter(df_cluster, x='city_development_index', y='experience', color='Cluster',
                     title='Segmentación de Candidatos')
    st.plotly_chart(fig)

# Funcionalidad 7: Regresión logística para predecir candidatos en búsqueda de empleo
def regresion_logistica(df):
    st.subheader("Modelo de Regresión Logística para Predicción de Búsqueda de Empleo")
    df_model = df[['city_development_index', 'training_hours', 'target']].dropna()
    X = df_model[['city_development_index', 'training_hours']]
    y = df_model['target']
    model = LogisticRegression()
    model.fit(X, y)
    st.write("Coeficientes del modelo:", model.coef_)
    st.write("Intercepto:", model.intercept_)

# Funcionalidad 8: Mapa de calor según índice de calidad de vida
def mapa_calor_ciudades(df):
    st.subheader("Mapa de Calor del Índice de Calidad de Vida en las Ciudades")
    fig = px.density_mapbox(df, lat="city_development_index", lon="city_development_index",
                            z="city_development_index", radius=10,
                            title="Mapa de Calor del Índice de Calidad de Vida",
                            mapbox_style="stamen-terrain")
    st.plotly_chart(fig)

# Función principal
def main():
    st.title("Análisis del Mercado Laboral en Ciencia de Datos")
    opciones = ["Selecciona una opción", "Cargar archivo", "Ingresar URL"]
    opcion = st.selectbox("Elige una opción", opciones)
    
    if opcion == "Cargar archivo":
        url = "https://raw.githubusercontent.com/Jordan-677/Jordan-677-App_con_ChatGPT/refs/heads/main/data_science_job.csv"
        df = cargar_datos(url)
        if df is not None:
            distribucion_puestos(df)
            mapa_ciudades(df)
            educacion_por_genero(df)
            industrias_ciencia_datos(df)
            clustering_ofertas(df)
            clustering_candidatos(df)
            regresion_logistica(df)
            mapa_calor_ciudades(df)
    elif opcion == "Ingresar URL":
        user_url = st.text_input("Ingresa la URL del archivo CSV:")
        if user_url:
            df = cargar_datos(user_url)
            if df is not None:
                distribucion_puestos(df)
                mapa_ciudades(df)
                educacion_por_genero(df)
                industrias_ciencia_datos(df)
                clustering_ofertas(df)
                clustering_candidatos(df)
                regresion_logistica(df)
                mapa_calor_ciudades(df)

if __name__ == "__main__":
    main()
