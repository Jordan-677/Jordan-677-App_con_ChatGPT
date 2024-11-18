import streamlit as st
import pandas as pd
import datetime

# Inicializar los datos
if 'registros' not in st.session_state:
    st.session_state.registros = pd.DataFrame(columns=["Fecha", "Tipo", "Categoría", "Monto", "Descripción"])

if 'presupuestos' not in st.session_state:
    st.session_state.presupuestos = pd.DataFrame(columns=["Mes", "Categoría", "Monto"])

if 'metas_ahorro' not in st.session_state:
    st.session_state.metas_ahorro = pd.DataFrame(columns=["Meta", "Monto Objetivo", "Monto Actual"])

# Función para agregar un registro de ingreso o gasto
def agregar_registro(tipo, categoria, monto, descripcion):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    nuevo_registro = pd.DataFrame([[fecha, tipo, categoria, monto, descripcion]], 
                                  columns=["Fecha", "Tipo", "Categoría", "Monto", "Descripción"])
    st.session_state.registros = pd.concat([st.session_state.registros, nuevo_registro], ignore_index=True)

# Función para agregar un presupuesto
def agregar_presupuesto(mes, categoria, monto):
    nuevo_presupuesto = pd.DataFrame([[mes, categoria, monto]], columns=["Mes", "Categoría", "Monto"])
    st.session_state.presupuestos = pd.concat([st.session_state.presupuestos, nuevo_presupuesto], ignore_index=True)

# Función para agregar una meta de ahorro
def agregar_meta(meta, monto_objetivo):
    nueva_meta = pd.DataFrame([[meta, monto_objetivo, 0.0]], columns=["Meta", "Monto Objetivo", "Monto Actual"])
    st.session_state.metas_ahorro = pd.concat([st.session_state.metas_ahorro, nueva_meta], ignore_index=True)

# Formulario para registrar ingresos/gastos
def formulario_registro():
    st.header("Registrar Ingreso o Gasto")
    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"], key="tipo_input")
    categoria = st.text_input("Categoría (Ejemplo: Alimentación, Transporte, etc.)", key="categoria_input")
    monto = st.number_input("Monto", min_value=0.01, format="%.2f", key="monto_input")
    descripcion = st.text_area("Descripción", key="descripcion_input")
    
    if st.button("Agregar Registro", key="agregar_registro_button"):
        agregar_registro(tipo, categoria, monto, descripcion)
        st.success(f"{tipo} registrado correctamente.")

# Formulario para presupuestos
def formulario_presupuesto():
    st.header("Establecer Presupuesto Mensual")
    mes = st.selectbox("Mes", [datetime.datetime.now().strftime("%B")], key="mes_input")  # Solo el mes actual para simplificar
    categoria = st.text_input("Categoría (Ejemplo: Alimentación, Transporte, etc.)", key="categoria_presupuesto_input")
    monto = st.number_input("Monto Presupuestado", min_value=0.01, format="%.2f", key="monto_presupuesto_input")
    
    if st.button("Agregar Presupuesto", key="agregar_presupuesto_button"):
        agregar_presupuesto(mes, categoria, monto)
        st.success(f"Presupuesto para {categoria} en {mes} agregado correctamente.")

# Formulario para metas de ahorro
def formulario_metas_ahorro():
    st.header("Establecer Meta de Ahorro")
    meta = st.text_input("Nombre de la Meta (Ejemplo: Vacaciones, Emergencias, etc.)", key="meta_input")
    monto_objetivo = st.number_input("Monto Objetivo", min_value=0.01, format="%.2f", key="monto_objetivo_input")
    
    if st.button("Agregar Meta", key="agregar_meta_button"):
        agregar_meta(meta, monto_objetivo)
        st.success(f"Meta de ahorro para {meta} agregada correctamente.")

# Función para generar reporte de diferencias
def generar_reporte():
    st.header("Reporte de Diferencias")
    
    # Filtrar por mes actual
    mes_actual = datetime.datetime.now().strftime("%B")
    
    # Datos reales
    ingresos = st.session_state.registros[st.session_state.registros["Tipo"] == "Ingreso"]
    gastos = st.session_state.registros[st.session_state.registros["Tipo"] == "Gasto"]
    
    ingresos_mes = ingresos[ingresos["Fecha"].str.contains(mes_actual)]
    gastos_mes = gastos[gastos["Fecha"].str.contains(mes_actual)]
    
    # Datos presupuestados
    presupuesto_mes = st.session_state.presupuestos[st.session_state.presupuestos["Mes"] == mes_actual]
    
    # Calcular las diferencias
    ingresos_real = ingresos_mes["Monto"].sum()
    gastos_real = gastos_mes["Monto"].sum()
    ingresos_presupuestado = presupuesto_mes[presupuesto_mes["Categoría"] == "Ingreso"]["Monto"].sum()
    gastos_presupuestado = presupuesto_mes[presupuesto_mes["Categoría"] == "Gasto"]["Monto"].sum()
    
    diferencia_ingresos = ingresos_real - ingresos_presupuestado
    diferencia_gastos = gastos_real - gastos_presupuestado
    
    st.write(f"**Ingresos reales:** {ingresos_real:.2f}")
    st.write(f"**Ingresos presupuestados:** {ingresos_presupuestado:.2f}")
    st.write(f"**Diferencia de ingresos:** {diferencia_ingresos:.2f}")
    
    st.write(f"**Gastos reales:** {gastos_real:.2f}")
    st.write(f"**Gastos presupuestados:** {gastos_presupuestado:.2f}")
    st.write(f"**Diferencia de gastos:** {diferencia_gastos:.2f}")

# Layout de la app
st.title("Gestión de Finanzas Personales")

# Sección para registrar ingresos y gastos
formulario_registro()

# Sección para establecer presupuestos
formulario_presupuesto()

# Sección para establecer metas de ahorro
formulario_metas_ahorro()

# Generar reportes de diferencias entre presupuestado y real
if st.button("Generar Reporte de Diferencias", key="generar_reporte_button"):
    generar_reporte()
