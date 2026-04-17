import streamlit as st
import pandas as pd
from datetime import datetime

from database import get_connection, crear_tablas
from scheduler import generar_horarios, ASESORAS

conn = get_connection()
crear_tablas(conn)

HORARIOS = generar_horarios()

st.set_page_config(page_title="Turnero Universidad")

# ---------------------------------

def asignar_turno(datos):

    fecha = datetime.today().strftime("%Y-%m-%d")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM turnos WHERE fecha=?",
        (fecha,)
    )

    usados = cursor.fetchone()[0]

    total = len(HORARIOS) * len(ASESORAS)

    if usados >= total:
        return None, None

    bloque = usados // len(ASESORAS)
    asesora = ASESORAS[usados % len(ASESORAS)]
    hora = HORARIOS[bloque].strftime("%H:%M")

   cursor.execute("""
INSERT INTO turnos(
    codigo,
    nombre,
    usuario,
    carrera,
    grupo,
    necesidad,
    hora,
    asesora,
    fecha,
    estado
)
VALUES(?,?,?,?,?,?,?,?,?,?)
""",
(
    datos["codigo"],
    datos["nombre"],
    datos["usuario"],
    datos["carrera"],
    datos["grupo"],
    datos["necesidad"],
    hora,
    asesora,
    fecha,
    "pendiente"
))

    conn.commit()

    return hora, asesora

# ---------------------------------

st.sidebar.info("Sistema de turnos estudiantes")

# ---------------------------------
# ESTUDIANTES
# ---------------------------------

st.title("Solicitar turno")

codigo = st.text_input("Código estudiante")
nombre = st.text_input("Nombre")

# ✅ NUEVO: tipo de usuario
usuario = st.selectbox("Tipo de usuario", ["Estudiante", "Docente"])

# ✅ NUEVO: lista de carreras
carreras = [
    "Ingeniería de Sistemas",
    "Administración Financiera",
    "Contaduría Pública",
    "Licenciatura en Educación Infantil",
    "Licenciatura en Literatura y Lengua Castellana",
    "Licenciatura en Educación Artística",
    "Licenciatura en Ciencias Naturales y Educación Ambiental",
    "Tecnología en Regencia de Farmacia"
]

carrera = st.selectbox("Carrera", carreras)

# ✅ ACTUALIZADO: más grupos
grupo = st.selectbox("Grupo", ["1", "2", "3", "4", "5"])

necesidad = st.text_area("Consulta")

if st.button("Solicitar turno"):

    datos = {
        "codigo": codigo,
        "nombre": nombre,
        "usuario": usuario,  # 👈 nuevo campo (por ahora no se guarda en BD)
        "carrera": carrera,
        "grupo": grupo,
        "necesidad": necesidad
        
    }

    hora, asesora = asignar_turno(datos)

    if hora is None:
        st.error("Turnos agotados")
    else:
        st.success("Turno asignado")

        st.info(f"""
Hora: {hora}

Te atenderá: {asesora}
""")

# ---------------------------------
# ADMIN
# ---------------------------------
# ---------------------------------
# ADMIN
# ---------------------------------




