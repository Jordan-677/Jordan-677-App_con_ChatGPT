import streamlit as st
import re

# Función para evaluar la fortaleza de la contraseña
def evaluar_contrasena(contrasena):
    # Expresión regular para validar una contraseña segura
    patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

    if re.match(patron, contrasena):
        return True, []
    else:
        sugerencias = []
        # Verificamos qué requisitos no se cumplen
        if len(contrasena) < 8:
            sugerencias.append("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[a-z]', contrasena):
            sugerencias.append("Debe incluir al menos una letra minúscula.")
        if not re.search(r'[A-Z]', contrasena):
            sugerencias.append("Debe incluir al menos una letra mayúscula.")
        if not re.search(r'\d', contrasena):
            sugerencias.append("Debe incluir al menos un número.")
        if not re.search(r'[@$!%*?&]', contrasena):
            sugerencias.append("Debe incluir al menos un carácter especial (@, $, !, %, *, ?, &).")

        return False, sugerencias

# Interfaz en Streamlit
st.title("Evaluador de Fortaleza de Contraseña")
st.write("Ingrese una contraseña para verificar su seguridad:")

# Entrada de la contraseña
contrasena = st.text_input("Contraseña", type="password")

if contrasena:
    es_segura, sugerencias = evaluar_contrasena(contrasena)
    
    if es_segura:
        st.success("¡La contraseña es segura!")
    else:
        st.error("La contraseña no cumple con los requisitos de seguridad.")
        st.write("Sugerencias para mejorarla:")
        for sugerencia in sugerencias:
            st.write(f"- {sugerencia}")
