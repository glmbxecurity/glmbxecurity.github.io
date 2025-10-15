---
title: "Rcpbind (Nfs)"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/rcpbind-(nfs)"
date: "2025-09-30"
---

### Identificar monturas NFS
Cuando se detecta el servicio rcpbind y nfs, se puede intentar investigar si hay monturas del sistema de ficheros de la máquina disponibles con:
```bash
showmount -e <ip>

nmap -p- <ip> --script nfs*
```

### Montar NFS en nuestro equipo
Si se ha detectado una montura, por ejemplo el directorio **/var** se puede montar en nuestra máquina.
```bash
mount <ip>:/var /ruta_local_donde_queremos_montar
"EJEMPLO"
mount 10.10.10.10:/var /prueba
```
