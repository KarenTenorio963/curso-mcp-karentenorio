import sys

def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else "Hola mundo"
    tokens_estimados = len(text) / 4
    print(f"Texto: '{text}'")
    print(f"Caracteres: {len(text)}")
    print(f"Tokens estimados: {tokens_estimados:.1f}")

if __name__ == "__main__":
    main()