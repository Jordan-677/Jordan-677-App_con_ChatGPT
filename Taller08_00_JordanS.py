import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import scipy.cluster.hierarchy as sch

def cargar_datos():
    """Carga datos desde archivo, URL o archivo de prueba."""
    opciones = {
        "Subir archivo": None, 
        "Desde URL": None, 
        "Archivo de prueba": "https://raw.githubusercontent.com/"
                           "gabrielawad/programacion-para-ingenieria/"
                           "refs/heads/main/archivos-datos/aplicaciones/"
                           "deforestacion.csv"
    }
    
    opcion = st.radio(
        "Selecciona la fuente de datos:", list(opciones.keys())
    )
    
    archivo = st.file_uploader("Sube un archivo CSV", type=["csv"])
    url = st.text_input("Ingresa la URL del archivo CSV")
    
    fuente = {
        "Subir archivo": archivo, 
        "Desde URL": url, 
        "Archivo de prueba": opciones["Archivo de prueba"]
    }
    return pd.read_csv(fuente[opcion])

def limpiar_datos(df):
    """Rellena valores faltantes mediante interpolación."""
    return df.interpolate()

def graficar_torta(df):
    """Genera gráfico de torta según tipo de vegetación."""
    conteo = df["Tipo_Vegetacion"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(
        conteo, 
        labels=conteo.index, 
        autopct='%1.1f%%', 
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

def mostrar_mapa(df, variable):
    """Muestra mapa de deforestación según variable."""
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.Longitud, df.Latitud)
    )
    fig, ax = plt.subplots()
    gdf.plot(column=variable, legend=True, cmap='OrRd', ax=ax)
    st.pyplot(fig)

def analisis_cluster(df):
    """Realiza análisis de clúster de superficies deforestadas."""
    matriz_distancia = sch.linkage(
        df[["Superficie_Deforestada"]], method='ward'
    )
    fig, ax = plt.subplots()
    sch.dendrogram(matriz_distancia, ax=ax)
    st.pyplot(fig)

def main():
    st.title("Análisis de la Deforestación")
    df = limpiar_datos(cargar_datos())
    st.write("Vista previa de los datos:")
    st.write(df.head())
    
    st.subheader("Gráfico de torta según tipo de vegetación")
    graficar_torta(df)
    
    variable = st.selectbox(
        "Selecciona una variable para el mapa", df.columns[3:]
    )
    st.subheader(f"Mapa de deforestación según {variable}")
    mostrar_mapa(df, variable)
    
    st.subheader("Análisis de Clúster")
    analisis_cluster(df)

if __name__ == "__main__":
    main()
