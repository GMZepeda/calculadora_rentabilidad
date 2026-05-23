import streamlit as st
import requests

# Título de la página web
st.title("Calculadora de Rentabilidad")
st.write("Ingrese los datos para calcular sus márgenes:")

# CAJITAS DE ENTRADA (Precio, Costo, Impuestos)
precio = st.number_input("Precio de venta ($)", min_value=0.0, step=100.0)
costo = st.number_input("Costo del producto ($)", min_value=0.0, step=100.0)
impuesto = st.number_input("Porcentaje de impuestos (%)", min_value=0.0, step=1.0)

# BOTÓN DE ACCIÓN
if st.button("Calcular"):
    
    # LA FLECHA DE IDA: Empaquetamos los datos en formato JSON
    datos_para_api = {
        "precio": precio,
        "costo": costo,
        "impuesto_porcentaje": impuesto
    }
    
    # Enviamos los datos al "Cerebro" (FastAPI)
    try:
        respuesta = requests.post("http://127.0.0.1:8000/calcular", json=datos_para_api)
        
        # LA FLECHA DE VUELTA: Recibimos el resultado y lo mostramos
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            st.success(f"**Ganancia Neta:** {resultado['ganancia_neta']}")
            st.info(f"**Margen:** {resultado['margen']}")
        else:
            st.error("Error: Verifique que los datos sean correctos y mayores a cero.")
            
    except requests.exceptions.ConnectionError:
        st.error("Error de conexión: ¿Está encendido el motor de la API?")