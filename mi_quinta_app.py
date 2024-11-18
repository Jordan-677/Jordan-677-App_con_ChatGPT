import streamlit as st
import pandas as pd
from datetime import datetime

# Título de la aplicación
st.title("Gestión de Asignaturas y Tareas")

# Autor
st.write("Esta app ha sido creada por Jordan Sánchez Torres.")

# Crear un contenedor para las asignaturas y tareas
if "asignaturas" not in st.session_state:
    st.session_state.asignaturas = {}

# Función para agregar asignatura
def agregar_asignatura(nombre_asignatura):
    if nombre_asignatura not in st.session_state.asignaturas:
        st.session_state.asignaturas[nombre_asignatura] = []
        st.success(f"Asignatura '{nombre_asignatura}' agregada exitosamente.")
    else:
        st.warning(f"La asignatura '{nombre_asignatura}' ya existe.")

# Función para agregar tarea a una asignatura
def agregar_tarea(asignatura, nombre_tarea, fecha_entrega):
    tarea = {
        "Nombre": nombre_tarea,
        "Fecha de entrega": fecha_entrega,
        "Completada": False
    }
    st.session_state.asignaturas[asignatura].append(tarea)
    st.success(f"Tarea '{nombre_tarea}' agregada a la asignatura '{asignatura}'.")

# Función para marcar tarea como completada
def marcar_completada(asignatura, index_tarea):
    st.session_state.asignaturas[asignatura][index_tarea]["Completada"] = True
    st.success(f"Tarea '{st.session_state.asignaturas[asignatura][index_tarea]['Nombre']}' marcada como completada.")

# Crear formulario para ingresar asignaturas
st.header("Agregar Asignatura")
nombre_asignatura = st.text_input("Nombre de la asignatura:")
if st.button("Agregar Asignatura"):
    if nombre_asignatura:
        agregar_asignatura(nombre_asignatura)
    else:
        st.warning("Por favor, ingresa el nombre de la asignatura.")

# Mostrar asignaturas existentes
if st.session_state.asignaturas:
    st.header("Asignaturas Existentes")
    for asignatura in st.session_state.asignaturas:
        st.subheader(asignatura)

        # Agregar tareas a la asignatura seleccionada
        with st.expander(f"Agregar tarea a '{asignatura}'"):
            nombre_tarea = st.text_input(f"Nombre de la tarea para '{asignatura}':", key=f"tarea_nombre_{asignatura}")
            fecha_entrega = st.date_input(f"Fecha de entrega para '{asignatura}':", min_value=datetime.today(), key=f"fecha_{asignatura}")
            if st.button(f"Agregar Tarea a {asignatura}", key=f"agregar_tarea_{asignatura}"):
                if nombre_tarea:
                    agregar_tarea(asignatura, nombre_tarea, fecha_entrega)
                else:
                    st.warning("Por favor, ingresa el nombre de la tarea.")

        # Mostrar tareas de la asignatura
        st.write("### Tareas de esta Asignatura:")
        tareas_df = pd.DataFrame(st.session_state.asignaturas[asignatura])
        if not tareas_df.empty:
            tareas_df["Completada"] = tareas_df["Completada"].apply(lambda x: "✔️" if x else "❌")
            st.dataframe(tareas_df)

            # Marcar tareas como completadas
            for i, tarea in enumerate(st.session_state.asignaturas[asignatura]):
                if tarea["Completada"] == False:
                    if st.checkbox(f"Marcar como completada: {tarea['Nombre']} (Fecha de entrega: {tarea['Fecha de entrega']})", key=f"completar_{asignatura}_{i}"):
                        marcar_completada(asignatura, i)
        else:
            st.write("No hay tareas registradas para esta asignatura.")
else:
    st.write("No se han registrado asignaturas aún. Por favor, agrega una asignatura primero.")
