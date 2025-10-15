---
title: "Waf"
layout: "single"
category: "Reconocimiento"
slug: "reconocimiento/waf"
date: "2025-09-30"
---

Web Application Firewall

### Wafw00f
Podemos determinar si una web está protegida bajo un WAF, como por ejemplo cloudflare. Esto nos puede servir para saber si la IP que hemos reconocido es real del servidor o no.
```bash
# Escaneo genérico
wafw00f miwerb.com

#Para realizar un full escaneo
wafw00f miweb.com -a
```

