---
title: "SNMP (161 UDP)"
layout: "single"
category: "Servicios"
slug: "servicios/snmp"
date: "2025-11-26"
---

### Community String
```bash
onesixtyone -c communities.txt <IP>
```

### Enumerar (Walk)
```bash
snmpwalk -v 2c -c public <IP>
snmp-check <IP> -c public
```
