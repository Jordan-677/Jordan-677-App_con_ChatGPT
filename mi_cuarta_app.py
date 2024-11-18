import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Cálculo del PAPA (Promedio Académico Ponderado Acumulado)")

# Autor
st.write("Esta app ha sido creada por Jordan Sánchez Torres.")

# Instrucciones para cargar el archivo CSV
st.subheader("Instrucciones para cargar el archivo CSV")
st.write("""
1. El archivo CSV debe tener las siguientes columnas en este orden:
   - `Materia`: El nombre de la asignatura.
   - `Calificación`: La calificación obtenida en la asignatura (por ejemplo, 4.5).
   - `Créditos`: El número de créditos de la asignatura (por ejemplo, 3).
   - `Tipología`: El tipo de asignatura (por ejemplo, "Disciplinar obligatoria").
2. Asegúrate de que el archivo esté en formato CSV y no contenga filas vacías ni errores de formato.
3. Una vez cargado el archivo, la app calculará el PAPA global y el PAPA por tipología.
""")

# Subir archivo CSV
uploaded_file = st.file_uploader("Carga tu archivo CSV", type=["csv"])

# Si se ha cargado un archivo, procesarlo
if uploaded_file is not None:
    # Leer el archivo CSV
    try:
        df = pd.read_csv(uploaded_file)
        # Validar que el archivo tiene las columnas correctas
        required_columns = ["Materia", "Calificación", "Créditos", "Tipología"]
        if all(col in df.columns for col in required_columns):
            st.success("Archivo CSV cargado correctamente.")
            
            # Mostrar los primeros registros del archivo cargado
            st.write("**Contenido del archivo cargado:**")
            st.dataframe(df.head())
            
            # Calcular el PAPA global
            total_calificacion = sum(df['Calificación'] * df['Créditos'])
            total_creditos = sum(df['Créditos'])
            papa_global = total_calificacion / total_creditos if total_creditos > 0 else 0
            
            # Mostrar el PAPA global
            st.write(f"**PAPA Global:** {papa_global:.2f}")
            
            # Calcular el PAPA por tipología
            st.write("**PAPA por Tipología:**")
            tipologias = df['Tipología'].unique()
            
            for tipologia in tipologias:
                df_tipologia = df[df['Tipología'] == tipologia]
                total_calificacion = sum(df_tipologia['Calificación'] * df_tipologia['Créditos'])
                total_creditos = sum(df_tipologia['Créditos'])
                papa_tipologia = total_calificacion / total_creditos if total_creditos > 0 else 0
                st.write(f"{tipologia}: {papa_tipologia:.2f}")
        else:
            st.error("El archivo CSV no tiene las columnas correctas. Por favor revisa el formato.")
    except Exception as e:
        st.error(f"Hubo un error al procesar el archivo: {e}")
else:
    st.write("Por favor carga tu archivo CSV para calcular el PAPA.")
