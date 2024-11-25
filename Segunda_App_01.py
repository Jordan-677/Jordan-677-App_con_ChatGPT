import streamlit as st
import re

def validar_nombre(nombre):
    """Valida si el nombre cumple con el formato esperado."""
    patron = r"^[A-Z][a-zA-Z]*$"
    return bool(re.match(patron, nombre))

def validar_email(email):
    """Valida si el correo electrónico cumple con el formato esperado."""
    patron = r"^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(patron, email))

def validar_telefono(telefono):
    """Valida si el número de teléfono cumple con el formato esperado."""
    patron = r"^\+?\d{7,15}$"
    return bool(re.match(patron, telefono))

def validar_fecha(fecha):
    """Valida si la fecha cumple con el formato DD/MM/AAAA."""
    patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
    return bool(re.match(patron, fecha))

# Interfaz de la app
st.title("Validación de Formularios Web")
st.write("Verifique la validez de los datos ingresados en un formulario web.")

nombre = st.text_input("Ingrese su nombre:")
email = st.text_input("Ingrese su correo electrónico:")
telefono = st.text_input("Ingrese su número de teléfono:")
fecha = st.text_input("Ingrese una fecha (DD/MM/AAAA):")

if st.button("Validar"):
    resultados = {
        "Nombre": "Válido" if validar_nombre(nombre) else "Inválido",
        "Correo electrónico": "Válido" if validar_email(email) else "Inválido",
        "Número de teléfono": "Válido" if validar_telefono(telefono) else "Inválido",
        "Fecha": "Válida" if validar_fecha(fecha) else "Inválida",
    }
    
    st.subheader("Resultados")
    for campo, resultado in resultados.items():
        st.write(f"{campo}: {resultado}")

st.caption("Creado por Jordan Sanchez Torres")
