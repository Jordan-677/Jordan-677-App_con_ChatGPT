import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import re
from scipy import stats

# Título de la aplicación
st.title("Aplicación para Visualizar Datos de Deforestación")

# Opción para cargar archivo
st.sidebar.header("Opciones")
cargar_datos = st.sidebar.button("Cargar archivo")

@st.cache_data
def cargar_archivo():
    """Carga el archivo CSV y muestra el contenido."""
    url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/deforestacion.csv"
    df = pd.read_csv(url)
    st.write("### Vista Previa del Archivo")
    st.dataframe(df.head())

cargar_datos and cargar_archivo()

