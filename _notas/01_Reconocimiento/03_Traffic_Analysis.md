---
title: "Traffic Analysis & PCAP"
layout: "single"
category: "Reconocimiento"
slug: "reconocimiento/traffic-analysis"
date: "2025-11-26"
---

Guía para analizar capturas de tráfico `.pcap` (Post-Explotación o CTF) y sniffing en tiempo real.

## 1. Búsqueda de Archivos (Post-Explotación)
Si ya tienes acceso a la máquina, busca capturas olvidadas. Suelen contener credenciales.

```bash
find / -name "*.pcap*" 2>/dev/null
```

## 2. Sniffing en tiempo real (Tcpdump)
Si eres root o estás en el grupo `pcap`/`netdev`.

```bash
# Ver tráfico en interfaz local (Loopback) - Útil para ver tráfico interno de servicios
tcpdump -i lo -v

# Guardar tráfico a fichero para analizar luego en Wireshark
tcpdump -i eth0 -w captura.pcap

# Leer fichero pcap por consola
tcpdump -r captura.pcap
```

## 3. Wireshark Cheatsheet

### Filtros Útiles
| Filtro | Descripción |
| :--- | :--- |
| `http.request.method == "POST"` | Ver formularios enviados (posibles logins). |
| `http.response.code == 200` | Ver respuestas exitosas. |
| `ip.addr == 10.10.10.5` | Filtrar por IP específica. |
| `tcp.port == 445` | Tráfico SMB. |
| `frame contains "password"` | Busca la cadena "password" en todo el paquete. |

### Extracción de Credenciales
1. **HTTP/Telnet/FTP:** El tráfico va en texto claro.
   * Click derecho en un paquete -> **Follow -> TCP Stream**.
   * Busca "User", "Pass", "Authorization".
2. **Strings:** Si no tienes Wireshark a mano, usa `strings` sobre el archivo pcap.
   ```bash
   strings captura.pcap | grep -iE "pass|pwd|login|user"
   ```
