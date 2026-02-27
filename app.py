import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Placas", layout="wide")
st.title("🔍 Consulta de Vehículos por Placa")

# URL pública de Google Sheets (formato CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRM2JtynG_FtyE4pbkLA1Fm5iWzxMPpx3-K6Y-oWSy_axDZ0-M-gHkBVfEDpUFc94Hpj6Svr1zbgCjs/pub?gid=95699436&single=true&output=csv"

@st.cache_data(ttl=600)  # Cache por 10 minutos
def cargar_datos():
    """Carga los datos desde Google Sheets y prepara la columna de placa."""
    try:
        df = pd.read_csv(SHEET_URL)
        if df.empty:
            st.warning("El archivo de datos está vacío.")
            return df
        # Asumimos que la primera columna es la placa
        col_placa = df.columns[0]
        # Convertir a string, mayúsculas y limpiar espacios
        df[col_placa] = df[col_placa].astype(str).str.upper().str.strip()
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return pd.DataFrame()

# Cargar datos
df = cargar_datos()

# Definir las columnas a mostrar (índices: A=0, B=1, C=2, G=6, H=7, I=8, P=15, Q=16, R=17, S=18, T=19, U=20, V=21, W=22, X=23, Y=24, Z=25, AA=26)
indices_columnas = [0, 1, 2, 6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

# Obtener los nombres de las columnas según los índices (si existen)
if not df.empty:
    nombres_columnas = df.columns.tolist()
    # Filtrar solo los índices que existen en el DataFrame
    indices_validos = [i for i in indices_columnas if i < len(nombres_columnas)]
    columnas_mostrar = [nombres_columnas[i] for i in indices_validos]
else:
    columnas_mostrar = []

# Interfaz de búsqueda
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        placa_input = st.text_input("Ingrese la placa a buscar:", placeholder="Ej: CMK035", key="placa").upper().strip()
    with col2:
        st.markdown("###")  # Espaciado vertical
        buscar = st.button("Buscar", type="primary")

# Resultados
if buscar:
    if placa_input == "":
        st.warning("Por favor ingrese una placa.")
    elif df.empty:
        st.error("No hay datos cargados.")
    else:
        # Filtrar por placa (columna 0)
        col_placa = df.columns[0]
        resultados = df[df[col_placa] == placa_input]
        
        if resultados.empty:
            st.warning(f"No se encontraron registros para la placa **{placa_input}**.")
        else:
            st.success(f"Se encontraron **{len(resultados)}** registro(s) para la placa **{placa_input}**.")
            
            # Mostrar solo las columnas seleccionadas
            if columnas_mostrar:
                resultados_mostrar = resultados[columnas_mostrar].fillna('')  # Reemplaza NaN por vacío
                st.dataframe(resultados_mostrar, use_container_width=True)
                
                # Botón de descarga
                #csv = resultados_mostrar.to_csv(index=False).encode('utf-8')
                #st.download_button(
                    #label="📥 Descargar resultados como CSV",
                    #data=csv,
                    #file_name=f"resultados_{placa_input}.csv",
                    #mime="text/csv"
                #)
            else:
                st.error("No se pudieron determinar las columnas a mostrar.")
else:
    # Mensaje inicial
    if not df.empty:
        st.info("Ingrese una placa y haga clic en Buscar.")
    else:
        st.stop()

# Mostrar vista previa opcional (expandible)
with st.expander("Ver vista previa de los datos (primeras 100 filas)"):
    if not df.empty:
        st.dataframe(df[columnas_mostrar].head(100) if columnas_mostrar else df.head(100))
        st.caption(f"Total de registros en la base: {len(df)}")
        #"Actualización del código con columnas específicas"

