from openrouter import preguntar_ia


def main():
    historial = []

    print("=== CHAT CON INTELIGENCIA ARTIFICIAL ===")
    print("Escribe 'salir' para terminar.")

    while True:
        pregunta = input("\nTú: ").strip()

        if pregunta.lower() == "salir":
            print("¡Hasta luego!")
            break

        if not pregunta:
            continue

        historial.append({
            "role": "user",
            "content": pregunta
        })

        respuesta = preguntar_ia(historial)

        if respuesta is not None:
            print("\nIA:", respuesta)

            historial.append({
                "role": "assistant",
                "content": respuesta
            })
        else:
            # Eliminar la pregunta si ha fallado la conexión
            historial.pop()


if __name__ == "__main__":
    main()
