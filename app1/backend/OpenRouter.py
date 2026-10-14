import requests
from config import API_KEY, URL, MODELO

def preguntar_ia(historial):
    cabeceras = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }

    datos = {
        "model": MODELO,
        "messages": historial
    }

    respuesta = requests.post(
        URL,
        headers=cabeceras,
        json=datos,
        timeout=60
    )

    if respuesta.status_code == 200:
        resultado = respuesta.json()
        return resultado["choices"][0]["message"]["content"]

    print("Error al conectar con OpenRouter:", respuesta.status_code)
    return None
