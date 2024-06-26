### Formulario de login
Cuando detectamos un panel de login, se pueden realizar varias cosas, probar inyecciones SQL, realizar fuerza bruta con wpscan (si se trata de un wordpress), tratar de enumerar usuarios con burpsuite, etc. En este caso vamos a tratar de hacer fuerza bruta al panel de login con **Burpsuite e Hydra** .

#### Interceptar petición

Realizamos un intento de login para interceptar la petición, nos interesan los campos `POST o  GET` junto con la `URL a la que se realizará el ataque`.  Además de la información que se tramita, normalmente algo parecido a `username=admin&password=admin`


* La ^PASS^ es una palabra reservada para que hydra haga la fuerza bruta en ese campo del formulario
* El mensaje de error, lo veremos al hacer un intento de login, lo podemos ver en la interfaz gráfica (esto lo necesita hydra para identificar cuando una pass es buena y cuando no)
* El proceso es lento, puede durar varios minutos hasta recorrer todo el diccionario.

```bash
hydra -t 64 -l admin -P <diccionario> <ip> http-post-form "/login.php:username=admin&password=^PASS^:<mensaje de error que nos da al meter una contraseña incorrecta>"
```

### Ventana emergente
Al llegar a un sitio web, puede que el navegador nos requiera de credenciales en forma de mini ventana emergente. Por ejemplo tenemos nos aparece una ventana emergente en  **http://ip/admin.php**
```bash
### para especificar usuario y pass por separado
hydra -l admin -P <diccionario> -s <port> -f <ip> http-get /admin.php

### para especificar usuario:pass en el mismo fichero
hydra -C <diccionario_user:pass> -s <port> -f <ip> http-get /admin.php
```