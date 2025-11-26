---
title: "Encoding & Decompiling"
layout: "single"
category: "Criptografia"
slug: "criptografia/encoding"
date: "2025-11-26"
---

### Base64
```bash
# Encodear
echo -n 'texto' | base64

# Decodear
echo -n 'dGV4dG8=' | base64 -d
```

### Lenguajes Esotéricos (CTF)
Si ves código raro repetitivo:

* **Ook!:** "Ook. Ook. Ook." -> [Decodificador](https://www.dcode.fr/ook-language)
* **Brainfuck:** `++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.` -> [Decodificador](https://www.dcode.fr/brainfuck-language)

### Ingeniería Inversa Básica
**Ghidra:**
Herramienta de la NSA para descompilar binarios (EXE/ELF) y ver código fuente aproximado (C/C++).
1.  Abrir Ghidra -> Nuevo Proyecto.
2.  Arrastrar el binario (Drag & Drop).
3.  Doble click y analizar.
