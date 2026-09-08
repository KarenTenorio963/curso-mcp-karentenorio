"""Paquete clase_sdd - Conversor de Temperatura."""

import sys
from clase_sdd.converter import convert_temperature, VALID_UNITS

__all__ = ["convert_temperature", "VALID_UNITS", "main"]


def main() -> None:
    """CLI interactivo para el conversor de temperatura."""
    print("=== Conversor de Temperatura (Spec-Driven Development) ===")
    print("Escalas válidas: Celsius (C), Fahrenheit (F), Kelvin (K)")
    
    if len(sys.argv) == 4:
        # Modo por línea de comandos: uv run clase-sdd <valor> <origen> <destino>
        val_arg, from_arg, to_arg = sys.argv[1], sys.argv[2], sys.argv[3]
        resultado = convert_temperature(val_arg, from_arg, to_arg)
        print(f"Resultado: {resultado}")
        return

    try:
        val = input("Ingrese el valor de temperatura: ")
        origen = input("Ingrese la escala de origen (C / F / K): ")
        destino = input("Ingrese la escala de destino (C / F / K): ")
        resultado = convert_temperature(val, origen, destino)
        print(f"Resultado: {resultado}")
    except (KeyboardInterrupt, EOFError):
        print("\nOperación cancelada.")
