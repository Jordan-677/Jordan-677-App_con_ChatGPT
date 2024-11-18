import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Cálculo del PAPA (Promedio Académico Ponderado Acumulado)")

# Autor
st.write("Esta app ha sido creada por Jordan Sánchez Torres.")

# Instrucciones para el usuario
st.subheader("Instrucciones")
st.write("""
1. Puedes calcular el PAPA de dos maneras:
   - **Cargar un archivo CSV** con las materias, calificaciones y créditos.
   - **Ingresar manualmente las materias**, calificaciones y créditos.

2. Si eliges cargar un archivo CSV, asegúrate de que el archivo tenga las siguientes columnas en este orden:
   - `Materia`: El nombre de la asignatura.
   - `Calificación`: La calificación obtenida en la asignatura (por ejemplo, 4.5).
   - `Créditos`: El número de créditos de la asignatura (por ejemplo, 3).
   - `Tipología`: El tipo de asignatura (por ejemplo, "Disciplinar obligatoria").
   
3. Una vez que cargues el archivo o ingreses las materias manualmente, la app calculará el PAPA global y el PAPA por tipología.
""")

# Opciones para el usuario: Cargar archivo o ingresar manualmente
opcion = st.radio("¿Cómo te gustaría calcular tu PAPA?", ("Cargar archivo CSV", "Ingresar manualmente"))

# Función para calcular el PAPA
def calcular_papa(df):
    total_calificacion = sum(df['Calificación'] * df['Créditos'])
    total_creditos = sum(df['Créditos'])
    papa_global = total_calificacion / total_creditos if total_creditos > 0 else 0
    
    # Calcular el PAPA por tipología
    papa_por_tipologia = {}
    tipologias = df['Tipología'].unique()
    
    for tipologia in tipologias:
        df_tipologia = df[df['Tipología'] == tipologia]
        total_calificacion = sum(df_tipologia['Calificación'] * df_tipologia['Créditos'])
        total_creditos = sum(df_tipologia['Créditos'])
        papa_por_tipologia[tipologia] = total_calificacion / total_creditos if total_creditos > 0 else 0
    
    return papa_global, papa_por_tipologia

# Si elige cargar un archivo CSV
if opcion == "Cargar archivo CSV":
    uploaded_file = st.file_uploader("Carga tu archivo CSV", type=["csv"])

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
                
                # Calcular el PAPA
                papa_global, papa_por_tipologia = calcular_papa(df)
                
                # Mostrar el PAPA global
                st.write(f"**PAPA Global:** {papa_global:.2f}")
                
                # Mostrar el PAPA por Tipología
                st.write("**PAPA por Tipología:**")
                for tipologia, papa in papa_por_tipologia.items():
                    st.write(f"{tipologia}: {papa:.2f}")
            else:
                st.error("El archivo CSV no tiene las columnas correctas. Por favor revisa el formato.")
        except Exception as e:
            st.error(f"Hubo un error al procesar el archivo: {e}")
    else:
        st.write("Por favor carga tu archivo CSV para calcular el PAPA.")

# Si elige ingresar las materias manualmente
else:
    st.subheader("Ingreso manual de materias")

    # Crear una lista para almacenar los datos ingresados
    materias = []
    calificaciones = []
    creditos = []
    tipologias = []

    while True:
        materia = st.text_input("Nombre de la materia:")
        if not materia:
            break  # Si el campo está vacío, terminamos el ingreso

        calificacion = st.number_input(f"Calificación de {materia}:", min_value=0.0, max_value=5.0, step=0.1)
        credito = st.number_input(f"Créditos de {materia}:", min_value=1, step=1)
        tipologia = st.selectbox(f"Tipología de {materia}:", ["Libre elección", "Disciplinar obligatoria", "Disciplinar optativa", "Fundamental obligatoria", "Fundamental optativa"])

        # Añadir los datos a las listas
        materias.append(materia)
        calificaciones.append(calificacion)
        creditos.append(credito)
        tipologias.append(tipologia)

        # Opción para añadir más materias
        if st.button("Añadir otra materia"):
            continue

    # Crear un DataFrame a partir de las listas
    if materias:
        df_manual = pd.DataFrame({
            "Materia": materias,
            "Calificación": calificaciones,
            "Créditos": creditos,
            "Tipología": tipologias
        })

        # Mostrar el DataFrame
        st.write("**Resumen de las materias ingresadas manualmente:**")
        st.dataframe(df_manual)

        # Calcular el PAPA
        papa_global, papa_por_tipologia = calcular_papa(df_manual)

        # Mostrar el PAPA global
        st.write(f"**PAPA Global:** {papa_global:.2f}")
        
        # Mostrar el PAPA por Tipología
        st.write("**PAPA por Tipología:**")
        for tipologia, papa in papa_por_tipologia.items():
            st.write(f"{tipologia}: {papa:.2f}")
    else:
        st.write("No se ha ingresado ninguna materia.")
