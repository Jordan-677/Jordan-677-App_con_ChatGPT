import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Función para llenar datos faltantes
def fill_missing_data(df):
    categorical_cols = df.select_dtypes(include=['object']).columns
    numerical_cols = df.select_dtypes(include=np.number).columns

    # Rellenar valores categóricos con la moda
    df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])

    # Rellenar valores numéricos
    # Calcular el porcentaje de valores nulos por columna
    null_percentage = df[numerical_cols].isna().mean()

    # Columnas con menos del 10% de valores nulos
    low_null_cols = null_percentage[null_percentage < 0.1].index
    # Columnas con 10% o más de valores nulos
    high_null_cols = null_percentage[null_percentage >= 0.1].index

    # Interpolación lineal para columnas con menos del 10% de valores nulos
    df[low_null_cols] = df[low_null_cols].apply(lambda col: col.interpolate(method='linear'))

    # Rellenar con la mediana para columnas con 10% o más de valores nulos
    df[high_null_cols] = df[high_null_cols].fillna(df[high_null_cols].median())

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

# Función para mostrar gráficos
def mostrar_graficos(df):
    st.subheader("Puestos de trabajo más comunes y su distribución según el tipo de compañía")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='job_title', hue='company_type', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader("Niveles de educación totales")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='education_level', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader("Niveles de educación discriminados por género")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='education_level', hue='gender', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader("Características de las industrias que ofrecen trabajo en ciencia de datos")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='industry', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

# Función para realizar clustering
def realizar_clustering(df):
    st.subheader("Clustering de ofertas de trabajo")
    features = df.select_dtypes(include=np.number).dropna(axis=1)
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(features)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=features.iloc[:, 0], y=features.iloc[:, 1], hue=df['cluster'], palette='viridis', ax=ax)
    st.pyplot(fig)

    st.subheader("Clustering de candidatos")
    candidate_features = df[['experience_years', 'education_level']].dropna()
    kmeans_candidates = KMeans(n_clusters=3, random_state=42)
    df['candidate_cluster'] = kmeans_candidates.fit_predict(candidate_features)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='experience_years', y='education_level', hue='candidate_cluster', data=df, palette='viridis', ax=ax)
    st.pyplot(fig)

# Función para realizar regresión logística
def realizar_regresion_logistica(df):
    st.subheader("Regresión logística para identificar características discriminantes de candidatos buscando empleo")
    df['looking_for_job'] = df['looking_for_job'].apply(lambda x: 1 if x == 'Yes' else 0)
    X = df.select_dtypes(include=np.number).drop(columns=['looking_for_job'])
    y = df['looking_for_job']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    st.write(f"Precisión del modelo: {accuracy:.2f}")

    coef = pd.DataFrame(model.coef_, columns=X.columns, index=['Coeficiente'])
    st.write("Coeficientes del modelo:")
    st.write(coef)

# Interfaz de Streamlit
st.title("Análisis de Ofertas de Trabajo en Ciencia de Datos")

st.sidebar.header("Cargar Datos")
upload_option = st.sidebar.radio("Selecciona una opción para cargar datos:", ("Subir archivo", "Usar URL"))

if upload_option == "Subir archivo":
    uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df = fill_missing_data(df)
        st.sidebar.success("Archivo cargado exitosamente!")
else:
    url = st.sidebar.text_input("Introduce la URL del archivo CSV", "https://raw.githubusercontent.com/Jordan-677/Jordan-677-App_con_ChatGPT/refs/heads/main/data_science_job.csv")
    if st.sidebar.button("Cargar datos"):
        df = cargar_datos(url)
        if df is not None:
            st.sidebar.success("Datos cargados exitosamente!")

if 'df' in locals():
    st.write("Datos cargados:")
    st.write(df.head())

    mostrar_graficos(df)
    realizar_clustering(df)
    realizar_regresion_logistica(df)
