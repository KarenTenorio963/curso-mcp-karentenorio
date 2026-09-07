"""Streaming response example with Gemini API."""

import os
import warnings

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Silenciar advertencias de AFC de la SDK
warnings.filterwarnings("ignore")

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.6-flash"


def main() -> None:
    response = client.models.generate_content_stream(
        model=MODEL,
        contents="Explica brevemente cómo funciona la arquitectura cliente-servidor.",
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=1000,
        ),
    )

    print("Respuesta en streaming:\n")
    for chunk in response:
        if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
            for part in chunk.candidates[0].content.parts:
                if part.text:
                    print(part.text, end="", flush=True)
    print("\n\n--- Fin del stream ---")


if __name__ == "__main__":
    main()