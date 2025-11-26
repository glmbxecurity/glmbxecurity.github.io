---
title: "RDP (3389)"
layout: "single"
category: "Servicios"
slug: "servicios/rdp"
date: "2025-11-26"
---

### Enumeración
```bash
nmap -p 3389 --script rdp-enum-encryption <IP>
use auxiliary/scanner/rdp/rdp_scanner
```

### Conexión
```bash
xfreerdp /u:<user> /p:<pass> /v:<IP> /cert:ignore
```

### BlueKeep (CVE-2019-0708)
RCE crítico en Win7/2008.
```bash
use exploit/windows/rdp/cve_2019_0708_bluekeep_rce
```
