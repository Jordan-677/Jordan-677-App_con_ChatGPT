import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
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
        df.columns = [
            "ID_Artefacto", "Nombre_Artefacto", "Material", "Edad_Aprox_Anios", "Ubicación_Descubrimiento", 
            "Latitud", "Longitud", "Cultura_Asociada", "Función_Estimada", "Técnica_Fabricación", 
            "Fecha_Descubrimiento", "Investigador_Principal", "Profundidad_Excavación_m", "Estado_Conservación", 
            "Patrones_Decorativos", "Método_Fechado"
        ]
        df_filled = fill_missing_data(df)
        st.write("Datos procesados:")
        st.dataframe(df_filled)
        mostrar_funcionalidades(df_filled)
    except FileNotFoundError:
        st.warning("Por favor, ingresa una URL válida.")
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")

# Función para cargar archivo desde una URL ingresada por el usuario
def cargar_desde_url():
    user_url = st.text_input("Ingresa la URL del archivo CSV:", placeholder="Esperando URL...")
    try:
        mostrar_datos(user_url)
    except ValueError:
        st.error("Error en la URL ingresada.")

# Mostrar funcionalidades de análisis y visualización
def mostrar_funcionalidades(df):
    st.header("Funcionalidades de Análisis y Visualización")

    checkboxes = [
        (st.checkbox("Mapa de calor de densidad (Técnica: Tallado)"), mostrar_mapa_calor),
        (st.checkbox("Gráfico de barras: Artefactos por Cultura"), mostrar_barras_cultura),
        (st.checkbox("Correlación Edad vs Profundidad"), mostrar_correlacion_edad_profundidad),
        (st.checkbox("Distribución de Materiales por Cultura"), mostrar_materiales_cultura),
        (st.checkbox("Mapa de dispersión: Ubicación de artefactos"), mostrar_mapa_dispersion),
        (st.checkbox("Patrones decorativos por Cultura"), mostrar_patrones_decorativos),
        (st.checkbox("Patrones temporales en descubrimientos"), mostrar_patrones_temporales)
    ]

    any(map(lambda cb: cb[1](df) if cb[0] else None, checkboxes))

# Funciones auxiliares para visualización
def mostrar_mapa_calor(df):
    tecnica_tallado = df[df["Técnica_Fabricación"] == "tallado"]
    numeric_cols = tecnica_tallado.select_dtypes(include=[np.number])
    try:
        plt.figure(figsize=(10, 6))
        sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm")
        st.pyplot(plt)
    except ValueError:
        st.warning("No hay suficientes columnas numéricas para generar el mapa de calor.")

def mostrar_barras_cultura(df):
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x="Cultura_Asociada", order=df["Cultura_Asociada"].value_counts().index)
    plt.xticks(rotation=45)
    st.pyplot(plt)

def mostrar_correlacion_edad_profundidad(df):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="Edad_Aprox_Anios", y="Profundidad_Excavación_m")
    plt.title("Correlación entre Edad Aproximada y Profundidad")
    st.pyplot(plt)

def mostrar_materiales_cultura(df):
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x="Material", hue="Cultura_Asociada")
    plt.xticks(rotation=45)
    st.pyplot(plt)

def mostrar_mapa_dispersion(df):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="Longitud", y="Latitud")
    plt.title("Ubicación Geográfica de los Artefactos")
    st.pyplot(plt)

def mostrar_patrones_decorativos(df):
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x="Patrones_Decorativos", hue="Cultura_Asociada")
    plt.xticks(rotation=45)
    st.pyplot(plt)

def mostrar_patrones_temporales(df):
    df["Fecha_Descubrimiento"] = pd.to_datetime(df["Fecha_Descubrimiento"], errors="coerce").dt.year
    plt.figure(figsize=(12, 6))
    sns.histplot(df["Fecha_Descubrimiento"].dropna(), bins=30, kde=True)
    plt.title("Distribución Temporal de Descubrimientos")
    st.pyplot(plt)

# Ejecutar acción seleccionada
acciones.get(opcion, lambda: None)()

