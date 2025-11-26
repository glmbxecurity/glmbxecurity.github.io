---
title: "File Upload Bypass"
layout: "single"
category: "Web Hacking"
slug: "web-hacking/file-upload"
date: "2025-11-26"
---

### Extensiones Alternativas
Si bloquean `.php`:
* `.php3`, `.php4`, `.php5`, `.phtml`, `.phar`

### Trucos de Nombre
* **Doble extensión:** `shell.php.png`
* **Null byte:** `shell.php%00.png`
* **Mayúsculas:** `shell.pHp`

### Magic Bytes (Mime Type)
Engañar al servidor para que crea que es una imagen.
1.  Añade `GIF89a;` al inicio del archivo.
2.  En Burp, cambia `Content-Type: application/x-php` a `image/gif`.
