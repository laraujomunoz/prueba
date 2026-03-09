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

        return None,None

    bloque = usados // len(ASESORAS)

    asesora = ASESORAS[usados % len(ASESORAS)]

    hora = HORARIOS[bloque].strftime("%H:%M")

    cursor.execute("""

    INSERT INTO turnos(
        codigo,nombre,carrera,grupo,
        necesidad,hora,asesora,fecha
    )

    VALUES(?,?,?,?,?,?,?,?)

    """,
    (
        datos["codigo"],
        datos["nombre"],
        datos["carrera"],
        datos["grupo"],
        datos["necesidad"],
        hora,
        asesora,
        fecha
    ))

    conn.commit()

    return hora,asesora

# ---------------------------------

st.sidebar.info("Sistema de turnos estudiantes")

# ---------------------------------
# ESTUDIANTES
# ---------------------------------


st.title("Solicitar turno")

codigo = st.text_input("Código estudiante")
nombre = st.text_input("Nombre")
carrera = st.text_input("Carrera")

grupo = st.selectbox("Grupo", ["1", "2"])

necesidad = st.text_area("Consulta")

if st.button("Solicitar turno"):

    datos = {
        "codigo": codigo,
        "nombre": nombre,
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



