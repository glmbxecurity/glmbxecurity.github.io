Cuando detectamos un panel de login, se pueden realizar varias cosas, probar inyecciones SQL, realizar fuerza bruta con wpscan (si se trata de un wordpress), tratar de enumerar usuarios con burpsuite, etc. En este caso vamos a tratar de hacer fuerza bruta al panel de login con **Burpsuite e Hydra** .

#### Interceptar petición

Realizamos un intento de login para interceptar la petición, nos interesan los campos `POST o  GET` junto con la `URL a la que se realizará el ataque`.  Además de la información que se tramita, normalmente algo parecido a `username=admin&password=admin`


* La ^PASS es una palabra reservada para que hydra haga la fuerza bruta en ese campo del formulario
* El mensaje de error, lo veremos al hacer un intento de login, lo podemos ver en la interfaz gráfica (esto lo necesita hydra para identificar cuando una pass es buena y cuando no)
* El proceso es lento, puede durar varios minutos hasta recorrer todo el diccionario.

```bash
hydra -t 64 -l admin -P <diccionario> http-post-form "/login.php:username=admin&password=^PASS:<mensaje de error que nos da al meter una contraseña incorrecta>"
```