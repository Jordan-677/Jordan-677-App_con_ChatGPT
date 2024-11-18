import streamlit as st

# Funciones de conversión
def convertir_temperatura(valor, de, a):
    if de == 'Celsius' and a == 'Fahrenheit':
        return (valor * 9/5) + 32
    elif de == 'Fahrenheit' and a == 'Celsius':
        return (valor - 32) * 5/9
    elif de == 'Celsius' and a == 'Kelvin':
        return valor + 273.15
    elif de == 'Kelvin' and a == 'Celsius':
        return valor - 273.15

def convertir_longitud(valor, de, a):
    if de == 'Pies' and a == 'Metros':
        return valor * 0.3048
    elif de == 'Metros' and a == 'Pies':
        return valor / 0.3048
    elif de == 'Pulgadas' and a == 'Centímetros':
        return valor * 2.54
    elif de == 'Centímetros' and a == 'Pulgadas':
        return valor / 2.54

def convertir_peso(valor, de, a):
    if de == 'Libras' and a == 'Kilogramos':
        return valor * 0.453592
    elif de == 'Kilogramos' and a == 'Libras':
        return valor / 0.453592
    elif de == 'Onzas' and a == 'Gramos':
        return valor * 28.3495
    elif de == 'Gramos' and a == 'Onzas':
        return valor / 28.3495

def convertir_volumen(valor, de, a):
    if de == 'Galones' and a == 'Litros':
        return valor * 3.78541
    elif de == 'Litros' and a == 'Galones':
        return valor / 3.78541
    elif de == 'Pulgadas cúbicas' and a == 'Centímetros cúbicos':
        return valor * 16.387
    elif de == 'Centímetros cúbicos' and a == 'Pulgadas cúbicas':
        return valor / 16.387

def convertir_tiempo(valor, de, a):
    if de == 'Horas' and a == 'Minutos':
        return valor * 60
    elif de == 'Minutos' and a == 'Segundos':
        return valor * 60
    elif de == 'Días' and a == 'Horas':
        return valor * 24
    elif de == 'Semanas' and a == 'Días':
        return valor * 7

def convertir_velocidad(valor, de, a):
    if de == 'Millas por hora' and a == 'Kilómetros por hora':
        return valor * 1.60934
    elif de == 'Kilómetros por hora' and a == 'Metros por segundo':
        return valor / 3.6
    elif de == 'Nudos' and a == 'Millas por hora':
        return valor * 1.15078
    elif de == 'Metros por segundo' and a == 'Pies por segundo':
        return valor * 3.28084

def convertir_area(valor, de, a):
    if de == 'Metros cuadrados' and a == 'Pies cuadrados':
        return valor * 10.7639
    elif de == 'Pies cuadrados' and a == 'Metros cuadrados':
        return valor / 10.7639
    elif de == 'Kilómetros cuadrados' and a == 'Millas cuadradas':
        return valor * 0.386102
    elif de == 'Millas cuadradas' and a == 'Kilómetros cuadrados':
        return valor / 0.386102

def convertir_energia(valor, de, a):
    if de == 'Julios' and a == 'Calorías':
        return valor * 0.239006
    elif de == 'Calorías' and a == 'Kilojulios':
        return valor / 239.006
    elif de == 'Kilovatios-hora' and a == 'Megajulios':
        return valor * 3.6
    elif de == 'Megajulios' and a == 'Kilovatios-hora':
        return valor / 3.6

def convertir_presion(valor, de, a):
    if de == 'Pascales' and a == 'Atmósferas':
        return valor / 101325
    elif de == 'Atmósferas' and a == 'Pascales':
        return valor * 101325
    elif de == 'Barras' and a == 'Libras por pulgada cuadrada':
        return valor * 14.5038
    elif de == 'Libras por pulgada cuadrada' and a == 'Bares':
        return valor / 14.5038

def convertir_datos(valor, de, a):
    if de == 'Megabytes' and a == 'Gigabytes':
        return valor / 1024
    elif de == 'Gigabytes' and a == 'Terabytes':
        return valor / 1024
    elif de == 'Kilobytes' and a == 'Megabytes':
        return valor / 1024
    elif de == 'Terabytes' and a == 'Petabytes':
        return valor / 1024

# Interfaz de usuario
st.title('Conversor Universal')

# Categoría de conversiones
categoria = st.selectbox('Selecciona una categoría:', [
    'Temperatura', 'Longitud', 'Peso/Masa', 'Volumen', 
    'Tiempo', 'Velocidad', 'Área', 'Energía', 'Presión', 'Tamaño de datos'])

if categoria == 'Temperatura':
    unidades = ['Celsius', 'Fahrenheit', 'Kelvin']
    unidad_origen = st.selectbox('Selecciona la unidad de origen:', unidades)
    unidad_destino = st.selectbox('Selecciona la unidad de destino:', unidades)
    valor = st.number_input('Introduce el valor:', float)

    if valor:
        resultado = convertir_temperatura(valor, unidad_origen, unidad_destino)
        st.write(f'{valor} {unidad_origen} = {resultado} {unidad_destino}')

elif categoria == 'Longitud':
    unidades = ['Pies', 'Metros', 'Pulgadas', 'Centímetros']
    unidad_origen = st.selectbox('Selecciona la unidad de origen:', unidades)
    unidad_destino = st.selectbox('Selecciona la unidad de destino:', unidades)
    valor = st.number_input('Introduce el valor:', float)

    if valor:
        resultado = convertir_longitud(valor, unidad_origen, unidad_destino)
        st.write(f'{valor} {unidad_origen} = {resultado} {unidad_destino}')

elif categoria == 'Peso/Masa':
    unidades = ['Libras', 'Kilogramos', 'Onzas', 'Gramos']
    unidad_origen = st.selectbox('Selecciona la unidad de origen:', unidades)
    unidad_destino = st.selectbox('Selecciona la unidad de destino:', unidades)
    valor = st.number_input('Introduce el valor:', float)

    if valor:
        resultado = convertir_peso(valor, unidad_origen, unidad_destino)
        st.write(f'{valor} {unidad_origen} = {resultado} {unidad_destino}')

elif categoria == 'Volumen':
    unidades = ['Galones', 'Litros', 'Pulgadas cúbicas', 'Centímetros cúbicos']
    unidad_origen = st.selectbox('Selecciona la unidad de origen:', unidades)
    unidad_destino = st.selectbox('Selecciona la unidad de destino:', unidades)
    valor = st.number_input('Introduce el valor:', float)

    if valor:
        resultado = convertir_volumen(valor, unidad_origen, unidad_destino)
        st.write(f'{valor} {unidad_origen} = {resultado} {unidad_destino}')

elif categoria == 'Tiempo':
    unidades = ['Horas', 'Minutos', 'Días', 'Semanas']
    unidad_origen = st.selectbox('Selecciona la unidad de origen:', unidades)
    unidad_destino = st.selectbox('Selecciona la unidad de destino:', unidades)
    valor = st.number_input('Introduce el valor:', float)

    if valor:
        resultado = convertir_tiempo(valor, unidad_origen, unidad_destino)
        st.write(f'{valor} {unidad_origen} = {resultado} {unidad_destino}')

elif categoria == 'Velocidad':
    unidades = ['Millas por hora', 'Kilómetros por hora', 'Nudos', 'Metros por segundo']
    unidad_origen = st.selectbox('Selecciona la unidad de origen:', unidades)
