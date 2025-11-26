---
title: "Windows Native (Netsh)"
layout: "single"
category: "Pivoting"
slug: "pivoting/windows-netsh"
date: "2025-11-26"
---

### Netsh PortProxy
Si comprometes un Windows y necesitas usarlo de puente sin subir herramientas. Requiere permisos de Administrador.

"Todo lo que llegue a la IP del Windows (Pivote) en el puerto 4444, envíalo a la IP Interna en el puerto 80".

```powershell
netsh interface portproxy add v4tov4 listenport=4444 listenaddress=0.0.0.0 connectport=80 connectaddress=10.10.10.5
```

**Verificar reglas:**
```powershell
netsh interface portproxy show all
```

**Borrar reglas:**
```powershell
netsh interface portproxy reset
```
