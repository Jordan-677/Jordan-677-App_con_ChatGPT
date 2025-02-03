import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import scipy.cluster.hierarchy as sch
import re

# Función para cargar datos desde un archivo CSV
@st.cache
def cargar_datos_csv(url):
    return pd.read_csv(url)

# Función para interpolar los valores faltantes según el tipo de columna
def interpolar(df):
    # Interpolación de columnas numéricas
    df[df.select_dtypes(include=[np.number]).columns] = df.select_dtypes(include=[np.number]).interpolate(method='linear')

    # Interpolación de columnas de tipo datetime
    df[df.select_dtypes(include=[np.datetime64]).columns] = df.select_dtypes(include=[np.datetime64]).interpolate(method='time')

    # Relleno de columnas categóricas con el valor más frecuente
    df[df.select_dtypes(include=[np.object]).columns] = df.select_dtypes(include=[np.object]).apply(lambda col: col.fillna(col.mode()[0]))

    return df

# Interfaz de usuario
st.title("Aplicación de Análisis de Deforestación")

# Opción para cargar un archivo CSV desde la computadora del usuario
archivo = st.file_uploader("Elige un archivo CSV", type=["csv"])

# Opción para ingresar una URL
url = st.text_input("O ingresa la URL del archivo CSV", "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv")

# Carga de datos mediante las funciones de las librerías, sin usar condicionales explícitos
df = pd.read_csv(archivo) if archivo else cargar_datos_csv(url)

# Muestra los datos cargados
st.write("Datos cargados:")
st.dataframe(df.head())

# Interpolación de los datos
df_interpolado = interpolar(df)

# Mostrar datos después de interpolación
st.write("Datos después de la interpolación:")
st.dataframe(df_interpolado.head())

# Visualización con matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df_interpolado["Longitud"], df_interpolado["Latitud"], c=df_interpolado["Superficie_Deforestada"], cmap="viridis")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.set_title("Distribución de Deforestación")
st.pyplot(fig)

# Clúster jerárquico con scipy
Z = sch.linkage(df_interpolado[["Latitud", "Longitud"]], method='ward')
fig2 = plt.figure(figsize=(10, 6))
sch.dendrogram(Z)
plt.title("Clúster Jerárquico de Ubicaciones")
st.pyplot(fig2)
