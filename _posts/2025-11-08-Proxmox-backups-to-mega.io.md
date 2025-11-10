---
layout: single
title: Backup Proxmox LXC and VM to Mega
date: 2025-09-30
categories:
  - projects
author: Edward Herrera Galamba
excerpt: Como respaldar tus MV y LXC en MEGA automáticamente
---
# 💾 Backup automático de contenedores LXC en Proxmox y subida a MEGA con MegaCMD

## 📋 Descripción

Este tutorial explica cómo **automatizar los backups de tus contenedores LXC en Proxmox** y **subirlos automáticamente a tu cuenta de MEGA** para guardarlos en la nube usando **MegaCMD**.

Consta de **dos scripts**:

1. `backup_all_lxc.sh` → Hace backups locales de todos los LXC en `/raid1/storage/dump`
    
2. `mega_backup.sh` → Sube esos backups a tu cuenta de MEGA, **sin eliminar nada en Mega** (borrado manual)
    

---

## 🧩 Requisitos previos

### 1. Crear la carpeta donde se guardarán los backups

```bash
mkdir -p /raid1/storage/dump
# Adapta la ruta a tu entorno
```

---

### 2. Instalar MegaCMD

1. Descarga el paquete oficial para Debian/Proxmox:
    

```bash
wget https://mega.nz/linux/MEGAsync/Debian_11.0/amd64/megacmd-xUbuntu_22.04_amd64.deb
sudo dpkg -i megacmd-xUbuntu_22.04_amd64.deb
sudo apt -f install -y  # Para resolver dependencias
```

2. Verifica la instalación e inicia sesión:
    

```bash
mega-login
```

> 🔹 Nota: Este tutorial usa **MegaCMD**, no `megatools`. Con MegaCMD no hay eliminación automática de archivos antiguos.

---

### 3. Crear script de backup local de LXC

Guarda este script como `/usr/local/bin/backup_all_lxc.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/raid1/storage/dump"
MAX_BACKUPS=1
LXC_LIST=$(/usr/sbin/pct list | awk 'NR>1 && $1 != 100 {print $1}')
DATE=$(date +%Y-%m-%d_%H-%M-%S)

echo "=== Inicio de backups: $DATE ==="

for CTID in $LXC_LIST; do
    echo "📦 Iniciando backup para CTID $CTID..."

    # Apagar contenedor
    if ! /usr/sbin/pct shutdown $CTID --timeout 30; then
        /usr/sbin/pct stop $CTID
    fi

    # Esperar apagado
    TIMEOUT=10
    WAITED=0
    while /usr/sbin/pct status $CTID | grep -q "status: running"; do
        [ $WAITED -ge $TIMEOUT ] && /usr/sbin/pct stop $CTID && break
        sleep 5
        WAITED=$((WAITED + 5))
    done

    # Backup
    vzdump $CTID --dumpdir $BACKUP_DIR --mode stop --compress zstd

    # Encender contenedor
    /usr/sbin/pct start $CTID
    sleep 5

    # Limitar backups locales
    ls -1t $BACKUP_DIR/vzdump-lxc-${CTID}-*.tar.zst | tail -n +$(($MAX_BACKUPS + 1)) | while read OLD_BACKUP; do
        rm -f "$OLD_BACKUP"
    done

done

echo "✅ Todos los backups completados a $(date +%H:%M:%S)"
```

Hazlo ejecutable:

```bash
chmod +x /usr/local/bin/backup_all_lxc.sh
```

---

### 4. Crear script de subida a MegaCMD

Guarda este script como `/usr/local/bin/mega_backup.sh`:

```bash
#!/bin/bash

LOCAL_DIR="/raid1/storage/dump"       # Cambia según tu entorno
REMOTE_DIR="/proxmox/dump"            # Carpeta en MEGA
LOGFILE="/var/log/mega_backup.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] === Iniciando subida MEGA ===" >> "$LOGFILE"

# Verificar MegaCMD
if ! command -v mega-put &>/dev/null; then
    echo "[$DATE] ERROR: megacmd no instalado" >> "$LOGFILE"
    exit 1
fi

[ ! -d "$LOCAL_DIR" ] && { echo "[$DATE] ERROR: No existe $LOCAL_DIR" >> "$LOGFILE"; exit 1; }

# Crear carpeta remota si no existe
mega-ls "$REMOTE_DIR" &>/dev/null || mega-mkdir -p "$REMOTE_DIR" >> "$LOGFILE" 2>&1

# Extraer ID de VM/LXC
extract_id() {
    echo "$1" | grep -oP 'vzdump-(lxc|qemu)-\K\d+'
}

# Comparar tamaño para decidir subir
file_needs_upload() {
    local local_file="$1"
    local remote_file="$2"
    local_size=$(stat -c %s "$local_file")
    remote_size=$(mega-ls "$REMOTE_DIR" | grep -F "$remote_file" | awk '{print $2}')
    [ -z "$remote_size" ] && return 0
    [ "$local_size" != "$remote_size" ] && return 0
    return 1
}

# Archivos locales
LOCAL_FILES=($(find "$LOCAL_DIR" -maxdepth 1 -type f \( -name "*.tar" -o -name "*.tar.zst" \) | sort))

for FILE in "${LOCAL_FILES[@]}"; do
    BASENAME=$(basename "$FILE")
    LOCAL_ID=$(extract_id "$BASENAME")
    [ -z "$LOCAL_ID" ] && { echo "[$DATE] ⏭️ Saltando $BASENAME" >> "$LOGFILE"; continue; }

    REMOTE_MATCHES=$(mega-ls "$REMOTE_DIR" | grep -E "vzdump-(lxc|qemu)-${LOCAL_ID}-")
    LATEST=""
    [ -n "$REMOTE_MATCHES" ] && LATEST=$(echo "$REMOTE_MATCHES" | sort | tail -n1)

    UPLOAD=false
    if [ -z "$LATEST" ] || file_needs_upload "$FILE" "$LATEST"; then
        UPLOAD=true
    else
        echo "[$DATE] ⏭️ $BASENAME sin cambios, nada que hacer" >> "$LOGFILE"
    fi

    $UPLOAD && {
        echo "[$DATE] Subiendo $BASENAME..." >> "$LOGFILE"
        mega-put "$FILE" "$REMOTE_DIR/" >> "$LOGFILE" 2>&1 && echo "[$DATE] ✅ Subido $BASENAME" >> "$LOGFILE"
    }

done

echo "[$DATE] === Subida completa (sin eliminar backups antiguos, se hará manualmente) ===" >> "$LOGFILE"
exit 0
```

Hazlo ejecutable:

```bash
chmod +x /usr/local/bin/mega_backup.sh
```

---

### 5. Pruebas manuales

```bash
/usr/local/bin/backup_all_lxc.sh
/usr/local/bin/mega_backup.sh
cat /var/log/mega_backup.log
```

---

### 6. Automatización con cron

```bash
0 2 * * * /usr/local/bin/backup_all_lxc.sh
0 4 * * * /usr/local/bin/mega_backup.sh
```

---

### 7. Consideraciones finales

- El script de subida **solo sube archivos nuevos o modificados**.
    
- **No elimina** ningún backup en MEGA; la limpieza de versiones antiguas es manual.
    
- Archivos remotos que no tengan equivalente local **permanecen intactos**.