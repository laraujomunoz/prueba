from datetime import datetime, timedelta, time

ASESORAS = ["Angela", "Graciela", "Lorena", "Lina"]

INICIO = time(7,0)
FIN = time(17,0)

ALMUERZO_INICIO = time(12,30)
ALMUERZO_FIN = time(13,0)


def generar_horarios():

    hoy = datetime.today().date()

    actual = datetime.combine(hoy, INICIO)
    fin = datetime.combine(hoy, FIN)

    horarios = []

    while actual < fin:

        if not(ALMUERZO_INICIO <= actual.time() < ALMUERZO_FIN):

            horarios.append(actual)

        actual += timedelta(minutes=10)

    return horarios
