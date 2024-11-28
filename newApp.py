import streamlit as st

# Configuración inicial de la app
st.set_page_config(page_title="Preguntas", layout="centered")

# Variables para manejar estados
if 'respuesta1' not in st.session_state:
    st.session_state.respuesta1 = None
if 'respuesta2' not in st.session_state:
    st.session_state.respuesta2 = None
if 'mensaje' not in st.session_state:
    st.session_state.mensaje = ""
if 'completado' not in st.session_state:
    st.session_state.completado = False

# Enunciado principal
st.markdown("## Hola corazón, responde las siguientes preguntas y me mandas screenshot a WhatsApp. 😊")

# Pregunta 1
st.markdown("### 1. Estoy invitando a Jordan a Pizza")
respuesta1 = st.radio(
    "Selecciona una opción:",
    ["Sí", "No"],
    key="respuesta1_radio"
)

if respuesta1 == "No":
    st.session_state.mensaje = (
        "❌ ¡Ups! Esa respuesta no es válida. Inténtalo de nuevo y elige la correcta. 😉"
    )
    st.session_state.respuesta1 = None
    st.session_state.completado = False
elif respuesta1 == "Sí":
    st.session_state.respuesta1 = "Sí"
    st.session_state.mensaje = "✅ Respuesta marcada con éxito."

st.markdown(st.session_state.mensaje)

# Solo mostrar la segunda pregunta si la primera fue correcta
if st.session_state.respuesta1 == "Sí":
    st.markdown("### 2. Es una cita?")
    respuesta2 = st.radio(
        "Selecciona una opción:",
        ["Sí", "No"],
        key="respuesta2_radio"
    )

    if respuesta2 in ["Sí", "No"]:
        st.session_state.respuesta2 = respuesta2

# Mostrar mensaje final solo si ambas respuestas están completas y correctas
if st.session_state.respuesta1 == "Sí" and st.session_state.respuesta2:
    st.markdown("### Muy bien, ya puedes tomarle screenshot 📸")
    st.session_state.completado = True

# Mensaje final opcional
if st.session_state.completado:
    st.success("Gracias por participar. 😄")

# Créditos
st.markdown("**Creado por Jordan Sanchez Torres**")

