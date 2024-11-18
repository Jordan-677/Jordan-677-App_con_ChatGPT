import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Cálculo del PAPA (Promedio Académico Ponderado Acumulado)")

# Autor
st.write("Esta app ha sido creada por Jordan Sánchez Torres.")

# Función para calcular el PAPA
def calcular_papa(df):
    # Calcular el PAPA global
    total_calificacion = sum(df['Calificación'] * df['Créditos'])
    total_creditos = sum(df['Créditos'])
    papa_global = total_calificacion / total_creditos if total_creditos > 0 else 0
    
    return papa_global

# Función para calcular el PAPA por tipología
def calcular_papa_tipologia(df, tipologia):
    df_tipologia = df[df['Tipología'] == tipologia]
    total_calificacion = sum(df_tipologia['Calificación'] * df_tipologia['Créditos'])
    total_creditos = sum(df_tipologia['Créditos'])
    papa_tipologia = total_calificacion / total_creditos if total_creditos > 0 else 0
    return papa_tipologia

# Entrada de datos para las materias
st.header("Ingreso de Materias")

# Crear un formulario para ingresar los datos de las materias
materias = []
materia_counter = 0  # Contador para asignar una key única

while True:
    materia = st.text_input(f"Nombre de la materia (dejar vacío para finalizar):", key=f"materia_{materia_counter}")
    if not materia:
        break
    
    calificacion = st.number_input(f"Calificación obtenida en {materia}:", min_value=0.0, max_value=5.0, format="%.1f", key=f"calificacion_{materia_counter}")
    creditos = st.number_input(f"Créditos de {materia}:", min_value=1, format="%d", key=f"creditos_{materia_counter}")
    tipologia = st.selectbox(f"Tipología de {materia}:", ['Libre elección', 'Disciplinar obligatoria', 'Disciplinar optativa', 'Fundamental obligatoria', 'Fundamental optativa'], key=f"tipologia_{materia_counter}")
    
    # Agregar los datos de la materia al arreglo de materias
    materias.append([materia, calificacion, creditos, tipologia])
    materia_counter += 1
    
# Crear un DataFrame con los datos ingresados
if len(materias) > 0:
    df_materias = pd.DataFrame(materias, columns=['Materia', 'Calificación', 'Créditos', 'Tipología'])
    st.write("**Datos Ingresados:**")
    st.dataframe(df_materias)

    # Calcular el PAPA global
    papa_global = calcular_papa(df_materias)
    st.write(f"**PAPA Global:** {papa_global:.2f}")
    
    # Calcular el PAPA por tipología
    st.write("**PAPA por Tipología:**")
    tipologias = ['Libre elección', 'Disciplinar obligatoria', 'Disciplinar optativa', 'Fundamental obligatoria', 'Fundamental optativa']
    
    for tipologia in tipologias:
        papa_tipologia = calcular_papa_tipologia(df_materias, tipologia)
        st.write(f"{tipologia}: {papa_tipologia:.2f}")
else:
    st.warning("Por favor ingresa algunas materias antes de calcular el PAPA.")

