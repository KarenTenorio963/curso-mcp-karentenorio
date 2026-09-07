"""Handling API errors gracefully with proper exception catching."""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError, ClientError, ServerError

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

# Modelo activo en el entorno
MODEL = "gemini-3.5-flash-lite"


def test_invalid_key() -> None:
    print("--- PRUEBA 1: Clave de API inválida ---")
    bad_client = genai.Client(api_key="INVALID_KEY_12345")
    try:
        bad_client.models.generate_content(
            model=MODEL,
            contents="Hola",
        )
    except ClientError as e:
        print(f"[OK] Error de cliente capturado correctamente ({e.code}): {e.message}\n")
    except APIError as e:
        print(f"[OK] Error de API capturado: {e}\n")


def test_system_instruction() -> None:
    print("--- PRUEBA 2: Consulta con system_instruction ---")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents="¿Cómo estás?",
            config=types.GenerateContentConfig(
                system_instruction="Eres un asistente muy formal que responde en una sola oración en español.",
                temperature=0.1,
                max_output_tokens=100,
            ),
        )
        print(f"Respuesta del modelo: {response.text}")
    except ServerError as e:
        print(f"[ERROR 5xx] El servidor no está disponible actualmente ({e.code}): {e.message}")
    except APIError as e:
        print(f"[ERROR API] Ocurrió un error en la solicitud: {e}")


def main() -> None:
    test_invalid_key()
    test_system_instruction()


if __name__ == "__main__":
    main()