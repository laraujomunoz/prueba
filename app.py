import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Placas", layout="wide")
st.title("🔍 Consulta de Vehículos por Placa")

# IMPORTANTE: Reemplaza con tu URL pública de Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRM2JtynG_FtyE4pbkLA1Fm5iWzxMPpx3-K6Y-oWSy_axDZ0-M-gHkBVfEDpUFc94Hpj6Svr1zbgCjs/pub?gid=95699436&single=true&output=csv"

@st.cache_data(ttl=600)
def cargar_datos():
    df = pd.read_csv(SHEET_URL)
    if not df.empty:
        col_placa = df.columns[0]
        df[col_placa] = df[col_placa].astype(str).str.upper().str.strip()
    return df

# Interfaz de búsqueda (copia el resto del código que te di antes)
# ...