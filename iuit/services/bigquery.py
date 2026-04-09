from google.cloud import bigquery
import uuid
from datetime import datetime

client = bigquery.Client.from_service_account_json("credentials.json")

TABLE_ID = "mi_proyecto.mi_dataset.formulario"

def insertar_datos(data):
    rows = [
        {
            "id": str(uuid.uuid4()),
            "nombre": data["nombre"],
            "documento": data["documento"],
            "telefono": data["telefono"],
            "correo": data["correo"],
            "direccion": data["direccion"],
            "observaciones": data["observaciones"],
            "fecha": datetime.utcnow().isoformat()
        }
    ]

    errors = client.insert_rows_json(TABLE_ID, rows)

    if errors:
        return False, errors
    return True, None