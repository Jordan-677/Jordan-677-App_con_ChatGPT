import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time

# Configuración inicial de la app
st.set_page_config(page_title="Preguntas", layout="centered")

# Inicialización de estados
if 'respuesta1' not in st.session_state:
    st.session_state.respuesta1 = None
if 'respuesta2' not in st.session_state:
    st.session_state.respuesta2 = None
if 'mensaje' not in st.session_state:
    st.session_state.mensaje = ""
if 'completado' not in st.session_state:
    st.session_state.completado = False
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# Función para reiniciar los estados al recargar
def reset_estado():
    st.session_state.respuesta1 = None
    st.session_state.respuesta2 = None
    st.session_state.mensaje = ""
    st.session_state.completado = False
    st.session_state.game_started = False

# Botón para recargar
st.button("Recargar app", on_click=reset_estado)

# Enunciado principal
st.markdown("## Hola corazón, responde las siguientes preguntas y me mandas screenshot a WhatsApp. 😊")

# Pregunta 1
st.markdown("### 1. Estoy invitando a Jordan a Pizza")
respuesta1 = st.radio(
    "Selecciona una opción:",
    options=["", "Sí", "No"],  # "" crea la opción vacía inicial
    index=0,  # Empieza siempre en la opción vacía
    format_func=lambda x: "Selecciona una opción" if x == "" else x,  # Personaliza el texto de la opción vacía
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
        options=["", "Sí", "No"],
        index=0,
        format_func=lambda x: "Selecciona una opción" if x == "" else x,
        key="respuesta2_radio"
    )

    if respuesta2 in ["Sí", "No"]:
        st.session_state.respuesta2 = respuesta2

# Mostrar mensaje final solo si ambas respuestas están completas y correctas
if st.session_state.respuesta1 == "Sí" and st.session_state.respuesta2:
    st.markdown("### Muy bien, ya puedes tomarle screenshot 📸")
    st.session_state.completado = True

# Mostrar el jueguito del dinosaurio
if st.session_state.completado:
   

    # Iniciar el juego solo si no ha sido iniciado
    if not st.session_state.game_started:
        st.session_state.game_started = True

    # Parámetros del juego
    canvas_result = st_canvas(
        stroke_width=2,
        stroke_color="#000000",
        background_color="#f4f4f4",
        height=200,
        width=700,
        drawing_mode="freedraw",
        key="canvas",
    )

    st.write("Intenta dibujar un dinosaurio o simplemente diviértete 😄")

# Créditos
st.markdown("**App creada por Jordan Sanchez Torres**")
