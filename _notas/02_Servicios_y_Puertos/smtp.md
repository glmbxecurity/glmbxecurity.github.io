---
title: "SMTP (25)"
layout: "single"
category: "Servicios"
slug: "servicios/smtp"
date: "2025-11-26"
---

### Enumeración de Usuarios
```bash
nc -nv <IP> 25
VRFY root
EXPN admin
```
O usa `auxiliary/scanner/smtp/smtp_enum`.
