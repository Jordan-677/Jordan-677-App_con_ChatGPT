import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import scipy.cluster.hierarchy as sch

# Función para cargar los datos
@st.cache
def cargar_datos(url):
    return pd.read_csv(url)

# Interfaz Streamlit
st.title("Aplicación de Análisis de Deforestación")

# Crear un contenedor para la carga de archivos
col1, col2 = st.columns(2)

# Columna 1: Subir archivo
archivo = col1.file_uploader("Elige un archivo CSV", type=["csv"])

# Columna 2: Cargar desde URL
url = col2.text_input("O ingresa la URL del archivo CSV", 
                     "https://github.com/gabrielawad/programacion-para-ingenieria/blob/main/archivos-datos/aplicaciones/deforestacion.csv?raw=true")

# Cargar datos de manera declarativa con Streamlit
df = archivo and pd.read_csv(archivo) or cargar_datos(url)

# Muestra los primeros registros del archivo cargado
st.write("Datos cargados:")
st.dataframe(df.head())

# Interpolación de los datos
# Rellenar valores vacíos utilizando interpolación lineal
df_interpolado = df.interpolate()

# Muestra los datos después de la interpolación
st.write("Datos después de la interpolación:")
st.dataframe(df_interpolado.head())

# Visualización con matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df_interpolado["Longitud"], df_interpolado["Latitud"], c=df_interpolado["Superficie_Deforestada"], cmap="viridis")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.set_title("Distribución de Deforestación")
st.pyplot(fig)

# Clúster jerárquico
Z = sch.linkage(df_interpolado[["Latitud", "Longitud"]], method='ward')
fig2 = plt.figure(figsize=(10, 6))
sch.dendrogram(Z)
plt.title("Clúster Jerárquico de Ubicaciones")
st.pyplot(fig2)
