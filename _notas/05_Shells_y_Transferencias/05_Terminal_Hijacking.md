---
title: "Terminal Hijacking (Trolling & Spy)"
layout: "single"
category: "Shells"
slug: "shells/terminal-hijacking"
date: "2025-11-26"
---

### Escribir en la terminal de otro usuario
Si eres root o el mismo usuario, puedes inyectar texto en su sesión. Útil para ingeniería social o confundir al admin.

**1. Identificar la sesión (PTS):**
```bash
w
# o
ls -l /dev/pts/
```

**2. Escribir en su terminal:**
Imagina que su sesión es `/dev/pts/1`.
```bash
echo "System Failure. Shutting down..." > /dev/pts/1
```

**3. Espiar su sesión (Script):**
```bash
script -f /dev/pts/1
```
