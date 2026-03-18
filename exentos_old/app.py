import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Placas o Recibo", layout="wide")
st.title("🔍 Consulta de Vehículos por Placa o Recibo Oficial")

# URL pública de Google Sheets (ajústala si es necesario)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSKGjA4X6O256blKvLFYHp9ojj34ePBNQnwj1K7icTqVDCY8WSO05FGG2Y0BM4zMboMj8cWQI4OAAL0/pub?output=csv"

@st.cache_data(ttl=600)
def cargar_datos():
    df = pd.read_csv(SHEET_URL)
    if not df.empty:
        # Limpiar nombres de columnas (por si tienen espacios)
        df.columns = df.columns.str.strip()
        # Asegurar que la placa sea string y mayúscula
        col_placa = df.columns[0]  # Asumimos que la primera columna es la placa
        df[col_placa] = df[col_placa].astype(str).str.upper().str.strip()
        # La columna de recibo oficial (columna I) puede ser tratada como string para búsqueda
        # Ajusta el nombre si es diferente
        # Por si acaso, identificamos la columna por posición (índice 8) si el nombre no es confiable
    return df

# Definir las columnas a mostrar (según tus índices: A,B,C,D,E,F,G,H,I,J,K,L)
# Mapeamos los índices a nombres de columna (si los nombres son confiables) o usamos índices
# Para simplificar, usaremos selección por posición con iloc
# Pero necesitamos los nombres reales de las columnas en el DataFrame para poder filtrar
# Vamos a obtener las columnas por nombre (si los nombres son consistentes)
# Si prefieres usar índices, cambia la lógica.

# Nombres esperados (ajusta según tu hoja real):
# Col0: Placa, Col1: ?, Col2: ?, Col6: ?, Col7: ?, Col8: Recibo_Oficial, Col15:?, etc.
# Es más seguro usar índices posicionales al final.
# Pero para el filtrado necesitamos saber qué columna es la de recibo.

def buscar(placa_o_recibo, criterio, df):
    """Filtra el DataFrame según el criterio y el valor."""
    if criterio == "Placa":
        col = df.columns[0]  # Primera columna
        return df[df[col].astype(str).str.upper() == placa_o_recibo.upper().strip()]
    else:  # Recibo Oficial
        # Identificar la columna de recibo (columna I, índice 8)
        # Puede tener nombre "Recibo_Oficial" o "Recibo Oficial" o similar.
        # Buscamos por nombre que contenga "Recibo" o usamos posición.
        # Opción 1: por posición (índice 8) - más robusto si los nombres cambian
        col_recibo = df.columns[8]  # Novena columna (índice 8)
        return df[df[col_recibo].astype(str).str.strip() == str(placa_o_recibo).strip()]

# Interfaz de búsqueda
with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        criterio = st.radio("Buscar por:", ["Placa", "Recibo Oficial"], horizontal=True)
    with col2:
        valor_busqueda = st.text_input("Ingrese el valor:", key="input_valor").strip()
    with col3:
        st.markdown("###")
        buscar_clicked = st.button("Buscar", type="primary")

# Cargar datos (caché)
df = cargar_datos()

# Lógica de búsqueda
if buscar_clicked and valor_busqueda:
    if df.empty:
        st.warning("No se pudieron cargar los datos.")
    else:
        with st.spinner("Buscando..."):
            resultados = buscar(valor_busqueda, criterio, df)
            
            if resultados.empty:
                st.warning(f"No se encontraron registros para **{valor_busqueda}** en **{criterio}**.")
            else:
                st.success(f"Se encontraron **{len(resultados)}** registro(s).")
                
                # Mostrar solo las columnas seleccionadas (por índice: 0,1,2,6,7,8,15,16,... hasta 26)
                # Como no tenemos nombres confiables, usaremos iloc para seleccionar por posición
                # Definimos los índices de columna que queremos mostrar (0-based)
                indices_mostrar = [0,1,2,3,4,5,6,7,8,9,10,11]
              
                # Asegurarse de que los índices existen en el DataFrame
                max_index = len(df.columns) - 1
                indices_validos = [i for i in indices_mostrar if i <= max_index]
                
                # Seleccionar esas columnas por posición
                resultados_mostrar = resultados.iloc[:, indices_validos]
                
                # Reemplazar NaN por vacío
                resultados_mostrar = resultados_mostrar.fillna('')
                
                # Mostrar tabla
                st.dataframe(resultados_mostrar, use_container_width=True)
                
                # (Opcional) Podríamos poner un botón de descarga si se desea, pero lo has quitado
                # st.download_button(...)  # Comentado o eliminado

# Vista previa de datos (opcional)
with st.expander("Ver vista previa de los datos (primeras 100 filas)"):
    if not df.empty:
        # Mostrar primeras 100 filas con las mismas columnas seleccionadas (opcional)
        # O podemos mostrar todo con fillna
        preview = df.head(100).fillna('')
        st.dataframe(preview, use_container_width=True)
    else:
        st.info("No hay datos para mostrar.")
