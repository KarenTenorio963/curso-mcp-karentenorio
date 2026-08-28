import sys
import shutil

def main() -> None:
    print("=== Semáforo del Entorno ===")
    print(f"[OK] Python versión: {sys.version.split()[0]}")

    uv_path = shutil.which("uv")
    if uv_path:
        print("[OK] uv está instalado y disponible")
    else:
        print("[ERROR] uv no encontrado en PATH")

    git_path = shutil.which("git")
    if git_path:
        print("[OK] Git está instalado y disponible")
    else:
        print("[ERROR] Git no encontrado en PATH")

if __name__ == "__main__":
    main()