from openrouter import preguntar_ia


def app():
    print("=== RESUMEN DE TEXTO ===")

    texto = input("\nTexto: ").strip()

    if not texto:
        print("No has escrito ningún texto.")
        return

    historial = [{
        "role": "user",
        "content": (
            "Resume el siguiente texto de forma clara y breve. "
            "Devuelve únicamente el resumen, sin explicaciones adicionales e intentado usar lo que sale en el texto:\n\n"
            + texto
        )
    }]

    respuesta = preguntar_ia(historial)

    if respuesta is not None:
        print("\nResumen:", respuesta)


if __name__ == "__main__":
    app()
