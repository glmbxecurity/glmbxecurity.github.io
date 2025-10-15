#!/usr/bin/env python3
"""
set_category_varios.py

Uso:
  # dry-run (muestra lo que haría)
  python3 set_category_varios.py /ruta/a/_notas/07-varios --dry

  # ejecutar cambios
  python3 set_category_varios.py /ruta/a/_notas/07-varios

Qué hace:
- Recorre todos los .md en la carpeta indicada (no recursivo por defecto).
- Crea un backup por archivo (filename.md.bak) antes de modificar.
- Si el archivo tiene frontmatter YAML (arranca con '---'), actualiza/añade:
    category: "Varios"
    slug: "varios/<slugified-filename>"
  preservando el resto de keys (title, layout, date, etc).
- Si no tiene frontmatter, lo crea con title/layout/category/slug/date (fecha de modificación).
- Opcional: --recursive para procesar subcarpetas.
"""
import argparse
import os
import re
from datetime import datetime
import codecs
import shutil

def slugify(s):
    s = s.lower()
    s = re.sub(r"[\/\\]+", " ", s)
    s = re.sub(r"[^a-z0-9\-_]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    s = s.strip("-")
    return s or "varios-note"

def read_text(path):
    with codecs.open(path, "r", "utf-8", errors="ignore") as f:
        return f.read()

def write_text(path, text):
    with codecs.open(path, "w", "utf-8") as f:
        f.write(text)

def parse_frontmatter(text):
    """
    Si hay frontmatter al inicio, devuelve (fm_dict, body)
    fm_dict: dict de pares string->string (no yaml completo, mínimo)
    Si no hay fm devuelve (None, text)
    """
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    fm_raw = parts[1].strip()
    body = parts[2].lstrip("\n")
    fm = {}
    for line in fm_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
        else:
            # línea que no tiene ':', ignorar
            continue
    return fm, body

def build_frontmatter(fm, body):
    # Ordena keys comunes primero para legibilidad
    order = ["title", "layout", "category", "slug", "date"]
    lines = []
    for k in order:
        if k in fm:
            lines.append(f'{k}: "{fm[k]}"')
    for k in fm:
        if k not in order:
            lines.append(f'{k}: "{fm[k]}"')
    return "---\n" + "\n".join(lines) + "\n---\n\n" + (body or "")

def process_file(path, dry=False):
    text = read_text(path)
    fm, body = parse_frontmatter(text)
    mtime = os.path.getmtime(path)
    date_iso = datetime.utcfromtimestamp(mtime).strftime("%Y-%m-%d")
    filename = os.path.splitext(os.path.basename(path))[0]
    slug_part = slugify(filename)

    if fm is None:
        # crear frontmatter mínimo
        new_fm = {
            "title": filename.replace("-", " ").replace("_", " ").title(),
            "layout": "single",
            "category": "Varios",
            "slug": f"varios/{slug_part}",
            "date": date_iso
        }
        new_text = build_frontmatter(new_fm, body)
        action = "CREAR FM"
    else:
        # actualizar sin borrar otras claves
        fm["category"] = "Varios"
        # si no existe slug o queremos forzarlo, setearlo
        fm["slug"] = f"varios/{slug_part}"
        if "layout" not in fm:
            fm["layout"] = "single"
        if "title" not in fm:
            fm["title"] = filename.replace("-", " ").replace("_", " ").title()
        if "date" not in fm:
            fm["date"] = date_iso
        new_text = build_frontmatter(fm, body)
        action = "UPDATE FM"

    if dry:
        print(f"[DRY] {action}: {path} -> category='Varios', slug='varios/{slug_part}'")
    else:
        # backup
        bak = path + ".bak"
        shutil.copy2(path, bak)
        write_text(path, new_text)
        print(f"[OK] {action}: {path} (backup: {os.path.basename(bak)})")

def main():
    parser = argparse.ArgumentParser(description="Forzar category: Varios en .md dentro de una carpeta")
    parser.add_argument("folder", nargs="?", default=".", help="Carpeta con .md (por defecto: carpeta actual)")
    parser.add_argument("--dry", action="store_true", help="Simular sin modificar archivos")
    parser.add_argument("--recursive", action="store_true", help="Procesar subcarpetas recursivamente")
    args = parser.parse_args()

    folder = os.path.abspath(args.folder)
    if not os.path.isdir(folder):
        print("Error: la ruta no es una carpeta válida:", folder)
        return

    if args.recursive:
        walker = []
        for root, dirs, files in os.walk(folder):
            for f in files:
                if f.lower().endswith(".md"):
                    walker.append(os.path.join(root, f))
    else:
        walker = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".md")]

    if not walker:
        print("No se encontraron archivos .md en", folder)
        return

    for p in walker:
        process_file(p, dry=args.dry)

if __name__ == "__main__":
    main()
