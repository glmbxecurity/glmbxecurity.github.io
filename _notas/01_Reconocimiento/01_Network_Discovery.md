---
title: "Network Discovery & Port Scanning"
layout: "single"
category: "Reconocimiento"
slug: "reconocimiento/network-discovery"
date: "2025-11-26"
---

Guía para descubrir hosts vivos, escanear puertos, identificar servicios y buscar exploits de infraestructura.

## 1. Host Discovery (Descubrir equipos)

### Capa 2 (ARP) - Red Local
Ideal para entornos locales o cuando estás pivotando.
```bash
# Escaneo ARP (Muy rápido y preciso en LAN)
arp-scan -I <interfaz> --localnet --ignoredups
netdiscover -P -i eth0
```

### Capa 3 (ICMP / TCP)
Ideal para descubrir equipos en rangos grandes o con firewalls.
```bash
# Ping Sweep (ICMP)
nmap -sn 10.10.0.0/24
fping -a -g 10.10.0.0/24 2>/dev/null

# TCP SYN Ping (Bypass bloqueo ICMP) - Simula conexión al puerto 80/443
nmap -sn -PS80,443,8080 10.10.0.0/24
masscan -p80,443 10.10.0.0/24 --rate=1000

# TCP ACK Ping
nmap -sn -PA 10.10.0.0/24
```

### Identificación de Máquinas Virtuales (MAC Address)
* **VMware:** `00:05:69`, `00:0C:29`, `00:1C:14`, `00:50:56`
* **VirtualBox:** `08:00:27`
* **Hyper-V:** `00:15:5D`

---

## 2. Nmap (Escaneo de Puertos)

### Flujo de Trabajo "PRO"
1. **Escaneo Rápido (Todos los puertos):**
   ```bash
   nmap -p- --open --min-rate 5000 -vvv -n -Pn 10.10.10.10 -oG allPorts
   ```
2. **Extract Ports (Función o comando):**
   ```bash
   # Extraer puertos del fichero grepable
   cat allPorts | grep -oP '\d{1,5}/open' | awk '{print $1}' FS='/' | xargs | tr ' ' ','
   ```
3. **Escaneo Profundo (Versiones y Scripts):**
   ```bash
   nmap -p<PUERTOS_EXTRAIDOS> -sC -sV -n -Pn 10.10.10.10 -oN targeted
   ```

### Escaneos Específicos (UDP y Scripts)
```bash
# Top puertos UDP (Lento, ten paciencia)
nmap -sU --top-ports 200 --min-rate 2000 -n -Pn 10.10.10.10

# Usar scripts de vulnerabilidad específicos
nmap --script "vuln" -p <puerto> <IP>
nmap --script "smb-vuln*" -p 445 <IP>
```

### Evasión de Firewall / IDS
Si obtienes muchos "filtered" o bloqueos.
```bash
# Fragmentar paquetes (rompe firmas IDS simples)
nmap -f -n -Pn <IP>
# MTU Personalizada (múltiplo de 8)
nmap --mtu 24 -n -Pn <IP>
# Spoofing de IP (necesitas control de red)
nmap -D 192.168.1.5,RND:5 <IP>
# Source Port (simular tráfico DNS o Web)
nmap --source-port 53 <IP>
```

---

## 3. Identificación de Servicios (Banner Grabbing)

Si Nmap no identifica la versión, interactúa manualmente.

```bash
# Conexión directa
nc -nv <IP> <PUERTO>

# Identificación Web por consola
whatweb http://<IP>
curl -I http://<IP>

# Identificación Sistema Operativo (TTL aproximado)
# Linux: ~64 | Windows: ~128 | Cisco: ~255
ping -c 1 <IP> 
```

---

## 4. Búsqueda de Exploits (Searchsploit)

Una vez tienes la versión del servicio (ej: *Apache 2.4.49*).

```bash
# Actualizar BBDD
searchsploit -u

# Búsqueda básica
searchsploit Apache 2.4

# Copiar el exploit al directorio actual
searchsploit -m <id>

# Ver el código del exploit (LEER ANTES DE USAR)
searchsploit -x <id>
```
