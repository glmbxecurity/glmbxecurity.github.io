---
title: Tareas Cron
layout: single
category: Linux PrivEsc
slug: linux-privesc/tareas-cron
date: 2025-09-30
---

```bash
ps -aux | grep cron
```

Cuando se ejecutan tareas cron pero no se pueden ver en el crontab, una forma es ejecutar el comando ps, tras unos segundos volverlo a ejecutar y ver la diferencia de procesos, así identificaremos si hay una tarea cron.

```bash
#!/bin/bash

# Crear un archivo temporal para guardar la salida anterior de ps
PREV_FILE=$(mktemp)

# Ejecuta ps por primera vez y guarda la salida
ps aux > "$PREV_FILE"

# Bucle infinito para monitorear los procesos en tiempo real
while true; do
  # Espera un intervalo de tiempo (por ejemplo, 60 segundos)
  sleep 1

  # Crear un archivo temporal para la salida actual
  CUR_FILE=$(mktemp)
  ps aux > "$CUR_FILE"

  # Compara la salida anterior con la actual y muestra las diferencias
  echo "Comparando procesos..."
  diff "$PREV_FILE" "$CUR_FILE"

  # Actualiza el archivo anterior con la salida actual para la próxima comparación
  mv "$CUR_FILE" "$PREV_FILE"
done

```