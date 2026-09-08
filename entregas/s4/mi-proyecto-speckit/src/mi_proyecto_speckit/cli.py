import sys
from mi_proyecto_speckit.converter import (
    Unit,
    convert_temperature,
    format_result,
    AbsoluteZeroError,
)


def run_cli(args=None) -> int:
    """Función de ejecución CLI."""
    if args is None:
        args = sys.argv[1:]

    if len(args) == 0:
        print("=== Convertidor de Unidades de Temperatura ===")
        print("Uso: mi-proyecto-speckit <valor> <origen: C|F|K> <destino: C|F|K>")
        print("Ejemplo: mi-proyecto-speckit 100 C F")
        return 0

    if len(args) < 3:
        print(
            "Error: Parámetros insuficientes. Debe proporcionar <valor> <origen> <destino>.",
            file=sys.stderr,
        )
        return 1

    val_str, from_u, to_u = args[0], args[1], args[2]

    try:
        resultado = convert_temperature(val_str, from_u, to_u)
        print(format_result(resultado))
        return 0
    except AbsoluteZeroError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        return 1


def main() -> None:
    sys.exit(run_cli())


if __name__ == "__main__":
    main()
