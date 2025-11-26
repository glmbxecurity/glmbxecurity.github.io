import os

BASE_DIR = "_notas"
RECON_DIR = os.path.join(BASE_DIR, "01_Reconocimiento")

# Archivos viejos a eliminar
FILES_TO_DELETE = [
    "busqueda-de-exploits.md",
    "descubrir-equipos-en-la-red.md",
    "dominios-y-emails.md",
    "google-dorks-cheatsheet.md",
    "nmap.md",
    "reconocimiento-web.md",
    "version-de-servicio-y-s.o.md",
    "waf.md",
    "wireshark.md"
]

def clean_recon():
    print("--- LIMPIANDO RECONOCIMIENTO ---")
    for file in FILES_TO_DELETE:
        file_path = os.path.join(RECON_DIR, file)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🗑️  BORRADO: {file}")
        else:
            print(f"⚠️  No encontrado: {file}")
    
    print("\nRecuerda ejecutar 'python3 sync_categories.py' para actualizar los títulos.")

if __name__ == "__main__":
    clean_recon()
