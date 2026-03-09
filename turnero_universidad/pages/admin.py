import streamlit as st
import pandas as pd
from database import get_connection
from config import ADMIN_PASSWORD


st.title("Panel Administrador")

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        if password == ADMIN_PASSWORD:
            st.session_state.login = True
        else:
            st.error("Contraseña incorrecta")

else:

    conn = get_connection()

    df = pd.read_sql_query("SELECT * FROM turnos", conn)

    st.subheader("Turnos")

    st.dataframe(df)

    if st.button("Llamar siguiente turno"):

    fecha = datetime.today().strftime("%Y-%m-%d")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT hora, asesora, nombre, necesidad
        FROM turnos
        WHERE fecha=?
        ORDER BY hora
        LIMIT 1
    """, (fecha,))

    turno = cursor.fetchone()

    if turno:

        st.success("Turno actual")

        st.info(f"""
Hora: {turno[0]}

Asesora: {turno[1]}

Estudiante: {turno[2]}

Consulta: {turno[3]}
""")

    else:

        st.warning("No hay turnos")
