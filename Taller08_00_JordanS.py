import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import re
from scipy import stats

# Título de la aplicación
st.title("Aplicación para Visualizar Datos de Deforestación")

# Opciones de carga
st.sidebar.header("Opciones")
cargar_datos = st.sidebar.button("Cargar archivo")

@st.cache_data
def cargar_archivo():
    """Carga el archivo CSV desde una URL fija y muestra el contenido."""
    url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"
    df = pd.read_csv(url)
    df = procesar_datos(df)
    st.write("### Vista Previa del Archivo")
    st.dataframe(df)

@st.cache_data
def cargar_archivo_por_url(url):
    """Carga un archivo CSV desde una URL ingresada y muestra el contenido."""
    try:
        df = pd.read_csv(url)
        df = procesar_datos(df)
        st.write("### Vista Previa del Archivo")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")

@st.cache_data
def procesar_datos(df):
    """Limpia los datos vacíos mediante interpolación y gestiona tipos de columnas."""
    # Asegurar el tipo de datos correcto
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors='coerce')  # Primera columna como fecha
    columnas_numericas = df.select_dtypes(include=[np.number]).columns

    # Interpolar valores numéricos y reemplazar valores faltantes
    df[columnas_numericas] = df[columnas_numericas].interpolate(method='linear', limit_direction='both')
    df[columnas_numericas] = df[columnas_numericas].fillna(df[columnas_numericas].mean())  # Rellenar valores extremos que no puedan interpolarse

    # Reemplazar valores faltantes en columnas no numéricas
    df.iloc[:, 4] = df.iloc[:, 4].fillna("Desconocido")  # Quinta columna como texto

    return df

cargar_datos and cargar_archivo()

url = st.sidebar.text_input("Ingrese la URL del archivo CSV")
url and cargar_archivo_por_url(url)

