import streamlit as st
import sys
import os

# Para poder importar services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.bigquery import insertar_datos

st.title("📋 Formulario")

with st.form("formulario"):
    nombre = st.text_input("Nombre")
    documento = st.text_input("Documento")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo")
    direccion = st.text_input("Dirección")
    observaciones = st.text_area("Observaciones")

    submit = st.form_submit_button("Guardar")

if submit:
    data = {
        "nombre": nombre,
        "documento": documento,
        "telefono": telefono,
        "correo": correo,
        "direccion": direccion,
        "observaciones": observaciones
    }

    success, error = insertar_datos(data)

    if success:
        st.success("✅ Guardado en BigQuery")
    else:
        st.error(f"❌ Error: {error}")