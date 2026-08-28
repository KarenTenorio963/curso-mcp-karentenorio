import sys

def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "Estudiante"
    print(f"¡Hola {name}! Bienvenido al curso.")

if __name__ == "__main__":
    main()