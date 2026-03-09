import streamlit as st
import pandas as pd
from database import connect
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

    conn = connect()

    df = pd.read_sql_query("SELECT * FROM turnos", conn)

    st.subheader("Turnos")

    st.dataframe(df)

    if st.button("Llamar siguiente turno"):

        c = conn.cursor()

        c.execute("""
        SELECT id FROM turnos
        WHERE estado='espera'
        ORDER BY numero ASC
        LIMIT 1
        """)

        turno = c.fetchone()

        if turno:

            c.execute(
                "UPDATE turnos SET estado='atendido' WHERE id=?",
                (turno[0],)
            )

            conn.commit()

            st.success("Turno llamado")

        else:

            st.info("No hay turnos pendientes")
