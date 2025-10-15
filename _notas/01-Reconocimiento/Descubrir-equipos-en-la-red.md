---
title: "Host discovery"
layout: "single"
category: "Reconocimiento"
slug: "reconocimiento/descubrir-equipos-en-la-red"
date: "2025-09-30"
---

### Escaneos ARP (de capa 2)

 ```bash
 arp-scan -I <interfaz> --localnet --ignoredups

netdiscover -P -i eth0 

 ```
Cuando tratamos de máquinas a partir de Windows 10, este es el emjor método ya que por defecto el ping viene capado por firewall. (es el mejor siempre que el equipo esté al alcance y no en otras redes).

### Ping scan (de capa 3)
```bash

nmap -sn <dir_red/mask>

nmap -Pn 10.10.0.5 (cuado no responde al ping)(Útil para escanear windows)

netdiscover -P -i eth0 -r 192.168.1.0/24 (debemos poner la dirección de red de la interfaz que queremos escanear)

fping -a -g 10.10.0.0/16 2>/dev/null
```

Tener en cuenta que **puede haber subnetting**, y esto no impide encontrar equipos en distintas redes.
En caso de haber segmentación de red, no se verian equipos de otra red. Por ejemplo, si tuvieramos la red 10.10.10.0/24 e hicieramos el scan de la siguiente manera: 
```bash
nmap -sn 10.10.0.0/16
```
en caso de haber un equipo, ej: 10.10.54.25/16, y estuviera activo, lo veríamos.
**Las maquinas virtuales comienzan con la mac 08:00:... y tener un branding de PCS Systemtechnik**

### TCP SYN Ping (Cuando hay un firewall bloqueando ICMP)
Se envían paquetes a un puerto específico (comunmente el 80), para detectar si el equipo está en línea. (no necesariamente el puerto debe estar abierto para que esto funcione). Este escaneo es más seguro que el Ping ScaN.
```bash
masscan -p80,8000-8100 10.0.0.0/8 --rate=10000
nmap -sn -PS 10.10.0.0/16 (se puede a una IP o a toda la red)
```

### TCP ACK Ping
```bash
nmap -sn -PA 10.10.0.0/16 (se puede a una IP o a toda la red)
```
### MAC's típicas de Máquina Virtual
* 08:00:XX:XX:XX:XX
* 00:0c:29:XX:XX:XX
#### Brandings de MV
* PCS Systemtechnik
* Vmware

