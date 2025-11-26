---
title: "Steganography"
layout: "single"
category: "Criptografia"
slug: "criptografia/steganography"
date: "2025-11-26"
---

### Análisis Básico
**Strings:**
Busca cadenas de texto imprimibles dentro de cualquier archivo binario (imágenes, ejecutables).
```bash
strings imagen.jpg | grep -i "pass"
strings -n 10 binario.exe  # Mínimo 10 caracteres
```

**File:**
Verifica qué es realmente el archivo.
```bash
file imagen.jpg
```

### Steghide
Para ocultar/extraer datos en imágenes (JPG) y Audio (WAV).
```bash
# Extraer info (A veces pide contraseña, prueba enter vacío)
steghide extract -sf imagen.jpg
```
