import streamlit as st
import time

# Estado inicial
if "question_1" not in st.session_state:
    st.session_state.question_1 = None
if "question_2" not in st.session_state:
    st.session_state.question_2 = None
if "force_yes" not in st.session_state:
    st.session_state.force_yes = False

# Encabezado
st.title("Hola, corazón")
st.write("Responde las siguientes preguntas y mándame un screenshot a WhatsApp .")

# Pregunta 1
st.subheader("Pregunta 1:")
response_1 = st.radio(
    "Estoy invitando a Jordan a pizza 🍕:",
    options=["", "Sí", "No"],
    index=0,
    key="question_1"
)

if response_1 == "No":
    st.warning("😏 Mmm... ¡esa no es la respuesta correcta!")
    time.sleep(2)  # Simula una pausa para forzar reinicio
    st.session_state.force_yes = True
    st.session_state.question_1 = None  # Restablecer pregunta 1
    st.experimental_rerun()
elif response_1 == "Sí":
    st.success("✅ Respuesta marcada con éxito.")

# Pregunta 2
if response_1 == "Sí":
    st.subheader("Pregunta 2:")
    response_2 = st.radio(
        "¿Es una cita? :",
        options=["", "Sí", "No"],
        index=0,
        key="question_2"
    )

# Resultado final
if response_1 == "Sí" and st.session_state.question_2:
    st.success("Muy bien, ya puedes tomarle screenshot .")

# Crédito
st.write("---")
st.write("App creada por **Jordan Sanchez Torres**")

