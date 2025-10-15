---
title: "SNMP"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/snmp"
date: "2025-09-30"
---

### Reconocimiento
Hay que recordar que SNMP funciona por UDP, así que el reconocimiento se debe realizar así:
```bash
nmap -sU --top-ports 1000 --min-rate 2000 -n -Pn <ip>
```

### Obtener clave de  comunidad
Esta clave se necesita para enumerar la información que podemos obtener de SNMP
```bash
onesixtyone -c <rockyou.txt>
```

### Enumerar SNMP
Aquí podemos descubrir algún dominio, credenciales, usuarios, etc
```bash
snmpwalk-v 2c -c <clave_comunity> <ip>
```

