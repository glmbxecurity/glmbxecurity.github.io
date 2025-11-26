---
title: "AD Services (SMB, LDAP, WinRM)"
layout: "single"
category: "Active Directory"
slug: "active-directory/services"
date: "2025-11-26"
---

### 1. SMB (445) - En contexto AD

**Enumeración de Shares:**
```bash
# Listar recursos y permisos
smbmap -H <IP> -u usuario -p password

# Listar recursivo
smbmap -H <IP> -u usuario -p password -R
```

**CrackMapExec (La navaja suiza):**
```bash
# Enumerar shares
crackmapexec smb <IP> -u user -p pass --shares

# Enumerar usuarios logueados
crackmapexec smb <IP> -u user -p pass --loggedon-users

# Ver política de contraseñas
crackmapexec smb <IP> -u user -p pass --pass-pol
```

**Rpcclient (Enumeración interna):**
```bash
rpcclient -U "usuario%password" <IP>
> enumdomusers   # Listar usuarios
> enumdomgroups  # Listar grupos
> querygroupmem  # Miembros de grupo
```

---

### 2. LDAP (389 / 636)

**Enumeración Manual:**
```bash
# Volcar todo el directorio
ldapsearch -x -H ldap://<IP> -D "usuario@dominio.local" -w "password" -b "DC=dominio,DC=local"

# Buscar cosas interesantes (passwords en descripción)
ldapsearch ... "(description=*pass*)"
```

---

### 3. WinRM (5985 / 5986)

**Conexión Remota (Shell):**
La mejor forma de administrar Windows desde Linux.
```bash
# Evil-WinRM (La mejor herramienta)
evil-winrm -i <IP> -u usuario -p password

# Con Hash
evil-winrm -i <IP> -u usuario -H <HASH>
```

**Fuerza Bruta WinRM:**
```bash
crackmapexec winrm <IP> -u users.txt -p passwords.txt
```
