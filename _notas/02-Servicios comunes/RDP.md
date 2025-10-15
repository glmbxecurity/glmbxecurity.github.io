---
title: "RDP"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/rdp"
date: "2025-09-30"
---

### Enumeracion
En ocasiones con el tipico nmap no se detecta RDP **muestra algo como: ssl/dec-notes?** o algo extraño, para ello hay un scanner específico de metasploit.

Si no se está seguro a que hacer referencia, lo mejor es pasarle el siguiente scan, ya que puede que estemos ante un RDP
```bash
use auxiliary/scanner/rdp/rdp_scanner
```

### Credenciales por fuerza bruta con Hydra
Si se tiene usuario es mas sencillo, ya que solo pasaremos la password, pero se puede probar con un listado de usuarios y contraseñas.
```bash
hydra -L usuarios.txt -P rockyou.txt rdp://<ip> -s <puerto>
```

### Conexion RDP
```bash
xfreerdp /u:<usuario> /p:<password> /v:<IP>:<puerto>
```
