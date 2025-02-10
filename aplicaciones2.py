import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
from sklearn.cluster import KMeans
from streamlit_folium import st_folium
from scipy.spatial.distance import pdist, squareform

# Función para llenar valores vacíos
def llenar_vacios_vectorizado(df):
    """
    Llena los valores vacíos en un DataFrame utilizando operaciones vectorizadas.
    """
    # Columnas categóricas: llenar con la moda
    columnas_categóricas = df.select_dtypes(include=['object']).columns
    df[columnas_categóricas] = df[columnas_categóricas].apply(lambda x: x.fillna(x.mode()[0]))

    # Columnas numéricas: llenar con la media o la moda según la columna (valores enteros)
    df['Ingreso_Anual_USD'] = df['Ingreso_Anual_USD'].fillna(int(df['Ingreso_Anual_USD'].mean()))
    df['Historial_Compras'] = df['Historial_Compras'].fillna(int(df['Historial_Compras'].mean()))
    df['Latitud'] = df['Latitud'].fillna(int(df['Latitud'].mean()))
    df['Longitud'] = df['Longitud'].fillna(int(df['Longitud'].mean()))
    df['Edad'] = df['Edad'].fillna(int(df['Edad'].mode()[0]))

    return df

# Título de la aplicación
st.title("Aplicación de Análisis de Clientes")

# Opciones del menú
opcion = st.radio("Selecciona una opción", ["Selecciona", "Cargar archivo", "Ingresar URL"])

acciones = {
    "Cargar archivo": lambda: "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv",
    "Ingresar URL": lambda: st.text_input("Ingresa la URL del archivo CSV")
}

url = acciones.get(opcion, lambda: None)()
resultado = (lambda: pd.read_csv(url), lambda: None)[url is None]()

try:
    df_lleno = llenar_vacios_vectorizado(resultado)
    st.write("### Datos cargados y procesados:")
    st.dataframe(df_lleno)

    # Análisis de correlación
    st.header("Análisis de Correlación")
    st.write("#### Correlación Global")
    correlacion_global = df_lleno[['Edad', 'Ingreso_Anual_USD']].corr()
    st.write(correlacion_global)

    def mostrar_correlacion_segmentada(segmento, variable):
        correlaciones_segmentadas = (
            df_lleno.groupby(segmento)[['Edad', 'Ingreso_Anual_USD']]  
            .corr().loc[pd.IndexSlice[:, variable], 'Ingreso_Anual_USD']
            .reset_index()
        )
        correlaciones_segmentadas.columns = [segmento, 'Variable', 'Correlación']
        st.write(correlaciones_segmentadas.drop(columns=['Variable']))

    st.write("#### Correlación Segmentada por Género")
    mostrar_correlacion_segmentada('Genero', 'Edad')

    st.write("#### Correlación Segmentada por Frecuencia de Compras")
    mostrar_correlacion_segmentada('Historial_Compras', 'Edad')

    # Mapas de ubicación
    st.header("Mapas de Ubicación")
    mapa_global = folium.Map(location=[df_lleno['Latitud'].mean(), df_lleno['Longitud'].mean()], zoom_start=6)
    ubicaciones = df_lleno[['Latitud', 'Longitud', 'Genero', 'Ingreso_Anual_USD']].dropna().values

    # Uso de numpy para vectorizar la adición de marcadores
    _ = [folium.Marker(location=[lat, lon], popup=f"{gen}, {ingreso} USD").add_to(mapa_global) for lat, lon, gen, ingreso in ubicaciones]
    
    st.write("#### Mapa Global")
    st_folium(mapa_global)

    # Mapa de calor según ingresos
    st.write("#### Mapa de Calor según Ingresos")
    mapa_calor = folium.Map(location=[df_lleno['Latitud'].mean(), df_lleno['Longitud'].mean()], zoom_start=6)
    heat_data = df_lleno[['Latitud', 'Longitud', 'Ingreso_Anual_USD']].values.tolist()
    HeatMap(heat_data).add_to(mapa_calor)
    st_folium(mapa_calor)

    # Clustering
    st.header("Análisis de Clúster")
    kmeans = KMeans(n_clusters=3, random_state=42).fit(df_lleno[['Edad', 'Ingreso_Anual_USD']])
    df_lleno['Cluster'] = kmeans.labels_
    st.write("#### Clúster de Frecuencia de Compras")
    st.dataframe(df_lleno[['Edad', 'Ingreso_Anual_USD', 'Cluster']])

    # Gráfico de barras por género y frecuencia de compra
    st.header("Gráfico de Barras")
    fig, ax = plt.subplots()
    df_lleno.groupby(['Genero', 'Historial_Compras']).size().unstack().plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # Cálculo de distancias
    st.header("Cálculo de Distancias")
    coordenadas = df_lleno[['Latitud', 'Longitud']].values
    distancias = squareform(pdist(coordenadas))
    st.write("#### Distancias entre compradores")
    st.write(distancias)
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
