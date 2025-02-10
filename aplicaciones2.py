import streamlit as st
import pandas as pd

# Función para llenar valores vacíos
def llenar_vacios_vectorizado(df):
    """
    Llena los valores vacíos en un DataFrame utilizando operaciones vectorizadas.
    """
    # Columnas categóricas: llenar con la moda
    columnas_categóricas = df.select_dtypes(include=['object']).columns
    df[columnas_categóricas] = df[columnas_categóricas].apply(lambda x: x.fillna(x.mode()[0]))

    # Columnas numéricas: llenar con la media o la moda según la columna
    df['Ingreso_Anual_USD'] = df['Ingreso_Anual_USD'].fillna(df['Ingreso_Anual_USD'].mean())
    df['Historial_Compras'] = df['Historial_Compras'].fillna(df['Historial_Compras'].mean())
    df['Latitud'] = df['Latitud'].fillna(df['Latitud'].mean())
    df['Longitud'] = df['Longitud'].fillna(df['Longitud'].mean())
    df['Edad'] = df['Edad'].fillna(df['Edad'].mode()[0])

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
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
