---
title: "Active Directory Enumeration"
layout: "single"
category: "Active Directory"
slug: "active-directory/enumeration"
date: "2025-11-26"
---

### 1. Sin Credenciales (Desde fuera)
Si solo tienes conexión de red pero no usuario.

**Enumeración de Usuarios (Kerbrute):**
Valida usuarios contra Kerberos (Puerto 88) de forma silenciosa.
```bash
# Enumerar usuarios válidos
./kerbrute_linux_amd64 userenum -d dominio.local --dc <IP_DC> users.txt

# Fuerza bruta de contraseñas (Cuidado con los bloqueos)
./kerbrute_linux_amd64 bruteuser -d dominio.local --dc <IP_DC> passwords.txt <usuario>
```

**SMB Null Session:**
```bash
smbclient -N -L //<IP>
smbmap -H <IP> -u "null"
enum4linux -a <IP>
```

**LDAP Anónimo:**
```bash
ldapsearch -x -H ldap://<IP> -b "DC=dominio,DC=local"
```


---

### 2. Con Credenciales (Desde dentro)
Una vez tienes un usuario válido (aunque sea low-priv).

**BloodHound (El mapa del tesoro):**
Recopila datos para visualizarlos en BloodHound.
```bash
# Desde Linux (Python ingestor)
bloodhound-python -d dominio.local -u usuario -p password -gc <IP_DC> -c All -ns <IP_DNS>

# Desde Windows (SharpHound)
.\SharpHound.exe -c All
```

**PowerView (PowerShell):**
Carga el script en memoria: `Import-Module .\PowerView.ps1`
```powershell
Get-NetDomain       # Info básica del dominio
Get-NetUser         # Listar usuarios
Get-NetComputer     # Listar ordenadores
Get-NetGroup        # Listar grupos
Get-NetGroupMember -GroupName "Domain Admins"  # ¿Quién es admin?
Find-LocalAdminAccess  # ¿Dónde soy admin local?
```

**Ldapdomaindump (HTML Report):**
```bash
ldapdomaindump -u 'dominio\usuario' -p 'password' <IP_DC>
```
---
#### Conectarse a un recurso SMB con o sin credenciales
```bash
smbclient //192.168.118.130/anonymous -U "anonymous"
```
