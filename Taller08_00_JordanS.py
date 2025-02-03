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
cargar_por_url = st.sidebar.button("Cargar por URL")

@st.cache_data
def cargar_archivo():
    """Carga el archivo CSV desde una URL fija y muestra el contenido."""
    url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"
    df = pd.read_csv(url)
    st.write("### Vista Previa del Archivo")
    st.dataframe(df)

@st.cache_data
def cargar_archivo_por_url(url):
    """Carga un archivo CSV desde una URL ingresada y muestra el contenido."""
    df = pd.read_csv(url)
    st.write("### Vista Previa del Archivo")
    st.dataframe(df)

cargar_datos and cargar_archivo()
cargar_por_url and st.text_input("Ingrese la URL del archivo CSV", key="url_input") and cargar_archivo_por_url(st.session_state.url_input)

