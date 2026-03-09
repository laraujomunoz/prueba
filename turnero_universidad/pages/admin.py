import streamlit as st
import pandas as pd
from datetime import datetime
from database import get_connection
from config import ADMIN_PASSWORD


st.title("Panel Administrador")

# ---------------------------------
# CONTROL DE LOGIN
# ---------------------------------

if "login" not in st.session_state:
    st.session_state.login = False


if not st.session_state.login:

    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        if password == ADMIN_PASSWORD:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")


# ---------------------------------
# PANEL ADMIN
# ---------------------------------

else:

    conn = get_connection()

    df = pd.read_sql_query("SELECT * FROM turnos", conn)

    st.subheader("Turnos registrados")

    # -------- COLORES POR ESTADO --------

    def colorear_estado(val):
        if val == "pendiente":
            return "background-color: #fff3cd"
        elif val == "atendido":
            return "background-color: #d4edda"
        return ""

    if not df.empty and "estado" in df.columns:
        st.dataframe(df.style.applymap(colorear_estado, subset=["estado"]))
    else:
        st.dataframe(df)

    st.divider()

    # ---------------------------------
    # BOTON LLAMAR SIGUIENTE TURNO
    # ---------------------------------

    if st.button("Llamar siguiente turno"):

        fecha = datetime.today().strftime("%Y-%m-%d")

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, hora, asesora, nombre, necesidad
            FROM turnos
            WHERE fecha=? AND estado='pendiente'
            ORDER BY hora
            LIMIT 1
        """, (fecha,))

        turno = cursor.fetchone()

        if turno:

            turno_id = turno[0]

            cursor.execute("""
                UPDATE turnos
                SET estado='atendido'
                WHERE id=?
            """, (turno_id,))

            conn.commit()

            st.success("Turno llamado")

            st.info(f"""
Hora: {turno[1]}

Asesora: {turno[2]}

Estudiante: {turno[3]}

Consulta: {turno[4]}
""")

        else:

            st.warning("No hay turnos pendientes")
