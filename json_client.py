"""Structured JSON response example using Pydantic schema."""

import os
import json
from typing import List
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.5-flash-lite"


# Definimos el esquema esperado de la respuesta
class ComponenteWeb(BaseModel):
    nombre: str = Field(description="Nombre del componente frontend o backend")
    tecnologia: str = Field(description="Tecnología o framework utilizado")
    rol: str = Field(description="Función principal dentro de la arquitectura")


class ArquitecturaSistema(BaseModel):
    proyecto: str
    componentes: List[ComponenteWeb]


def main() -> None:
    response = client.models.generate_content(
        model=MODEL,
        contents="Genera el diseño conceptual para una aplicación de catálogo web de autos.",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ArquitecturaSistema,
            temperature=0.2,
        ),
    )

    print("Respuesta JSON recibida:\n")
    print(response.text)

    # Validamos que sea un JSON parseable en Python
    datos = json.loads(response.text)
    print("\n--- JSON parseado correctamente ---")
    print(f"Proyecto: {datos.get('proyecto')}")
    print(f"Número de componentes: {len(datos.get('componentes', []))}")


if __name__ == "__main__":
    main()