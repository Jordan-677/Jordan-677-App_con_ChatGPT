import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsRegressor

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsRegressor

# Función para llenar datos faltantes
def fill_missing_data(df):
    """
    Fills missing data in a DataFrame based on correlations.
    
    Args:
        df (DataFrame): DataFrame con datos a llenar.
    
    Returns:
        DataFrame: DataFrame con datos llenos.
    """
    categorical_cols = df.select_dtypes(include=['object']).columns
    numerical_cols = df.select_dtypes(include=np.number).columns

    # Imputación categórica
    df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])

    # Codificación de etiquetas
    data_for_imputation = df.copy()
    le = LabelEncoder()
    data_for_imputation[categorical_cols] = data_for_imputation[categorical_cols].apply(le.fit_transform)

    # Imputación KNN
    imputer = KNeighborsRegressor(n_neighbors=5)
    data_for_fitting = data_for_imputation.dropna()

    # Entrenar el modelo KNN
    imputer.fit(data_for_fitting.drop(numerical_cols, axis=1), data_for_fitting[numerical_cols])

    # Filtrar filas con NaNs
    rows_with_nan = data_for_imputation[numerical_cols].isna().any(axis=1)
    df.loc[rows_with_nan, numerical_cols] = imputer.predict(
        data_for_imputation.loc[rows_with_nan].drop(numerical_cols, axis=1)
    )

    return df

# Interfaz en Streamlit
st.title("Aplicación para Cargar y Procesar Datos")

# Menú de selección
opciones = ["Selecciona una opción", "Cargar archivo", "Ingresar URL"]
opcion = st.selectbox("Elige una opción", opciones)

acciones = {
    "Selecciona una opción": lambda: st.warning("Selecciona una opción para continuar."),
    "Cargar archivo": lambda: mostrar_datos("https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/datos_arqueologicos.csv"),
    "Ingresar URL": lambda: cargar_desde_url()
}

# Función para mostrar datos desde una URL
def mostrar_datos(url):
    try:
        df = pd.read_csv(url)
        df_filled = fill_missing_data(df)
        st.write("Datos procesados:")
        st.dataframe(df_filled)
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")

# Función para cargar archivo desde una URL ingresada por el usuario
def cargar_desde_url():
    user_url = st.text_input("Ingresa la URL del archivo CSV:")
    st.info("Esperando URL...") if not user_url else mostrar_datos(user_url)

# Ejecutar acción seleccionada
acciones.get(opcion, lambda: None)()
