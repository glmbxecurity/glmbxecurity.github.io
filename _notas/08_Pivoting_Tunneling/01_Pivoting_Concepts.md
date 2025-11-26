---
title: "Pivoting Basics & Proxychains"
layout: "single"
category: "Pivoting"
slug: "pivoting/basics"
date: "2025-11-26"
---

### Concepto
Usar una máquina comprometida (Pivot/Jump Host) para acceder a redes internas que no son visibles desde tu Kali.

* **Port Forwarding:** Traer un puerto específico de la víctima a tu máquina (1 a 1).
* **Dynamic Forwarding (SOCKS):** Crear un túnel para acceder a *toda* la red remota.

### Configurar Proxychains
Para usar herramientas (Nmap, Hydra) a través del túnel SOCKS.

**1. Editar configuración:** `/etc/proxychains4.conf`
```bash
# Comentar 'strict_chain'
# Descomentar 'dynamic_chain'
dynamic_chain
# Al final del archivo, añadir el puerto de tu túnel (ej: 1080)
socks5  127.0.0.1 1080
```

**2. Ejecutar herramientas:**
```bash
proxychains nmap -sT -Pn -p 445 10.10.10.5
# NOTA: Nmap a través de proxychains es LENTO y NO soporta SYN scan (-sS). Usa -sT.
```

### Barrido de Ping (Bash Script)
Si no tienes Nmap en la máquina pivot, sube este script o pégalo en la terminal para descubrir hosts vivos.
```bash
#!/bin/bash
for i in {1..254}; do
    timeout 1 bash -c "ping -c 1 10.10.10.$i" >/dev/null
    if [ $? -eq 0 ]; then
        echo "Host 10.10.10.$i is UP"
    fi
done
```
