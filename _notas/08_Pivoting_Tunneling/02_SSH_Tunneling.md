---
title: "SSH Tunneling (Native)"
layout: "single"
category: "Pivoting"
slug: "pivoting/ssh"
date: "2025-11-26"
---

Si tienes credenciales SSH de la máquina pivote, esta es la forma más estable.

### 1. Local Port Forwarding (-L)
"Quiero acceder al puerto 80 del servidor interno (10.10.10.5), trayéndolo a mi puerto 8080".

```bash
# Sintaxis: -L PuertoLocal:IP_Objetivo:PuertoObjetivo
ssh usuario@<IP_PIVOTE> -L 8080:10.10.10.5:80
```
*Ahora accede a `localhost:8080` en tu Kali.*

### 2. Dynamic Port Forwarding (-D) [SOCKS Proxy]
"Quiero montar un proxy SOCKS en mi puerto 1080 para acceder a TODA la red interna".

```bash
ssh usuario@<IP_PIVOTE> -D 1080
```
*Configura `/etc/proxychains.conf` con `socks5 127.0.0.1 1080`.*

### 3. Remote Port Forwarding (-R)
"Quiero que la víctima se conecte a mí y me ofrezca un puerto interno". (Útil si la víctima no tiene SSH server pero tú sí, o firewall bloquea entrada).

```bash
# En la máquina víctima:
ssh usuario@<TU_IP_KALI> -R 8080:127.0.0.1:80
```
