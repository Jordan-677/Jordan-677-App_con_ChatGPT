import streamlit as st

# Título de la app
st.title('Mi primera app')

# Autor de la app
st.markdown('Esta app fue elaborada por **Jordan Sanchez Torres**.')

# Preguntar el nombre al usuario
nombre_usuario = st.text_input('¿Cuál es tu nombre?')

# Mostrar un mensaje de bienvenida si el usuario ingresa su nombre
if nombre_usuario:
    st.write(f'{nombre_usuario}, te doy la bienvenida a mi primera app.')
