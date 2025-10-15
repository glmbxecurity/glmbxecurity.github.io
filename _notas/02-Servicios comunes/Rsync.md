---
title: "Rsync"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/rsync"
date: "2025-09-30"
---

# Rsync
 rsync is a utility for efficiently transferring and synchronizing files between a computer and an external hard drive and across networked computers

### Enumeración
```bash
nc -vn <ip> 873
```

### Comandos básicos

#### Listar directorios
```bash
al conectarme con nc nos aparece lo siguiente:
┌──(root㉿kali)-[~]
└─# nc -vn 10.10.157.39 873
(UNKNOWN) [10.10.157.39] 873 (rsync) open
@RSYNCD: 31.0 ##ESTO ES IMPORTANTE



SI COPIAMOS Y PEGAMOS '@RSYNCD: 31.0' NOS DEVUELVE EL DIRECTORIO O DIRECTORIOS DISPONIBLES. (es un poco raro, lo sé pero así funciona).
```

#### Conectarse 
```bash
rsync rsync://rsync-connect@ip/directorio_encontrado/

si vamos encontrando directorios
rsync rsync://rsync-connect@ip/directorio_encontrado/segundo_directorio/

##IMPORTANTE EL SLASH FINAL, SINO NO MUESTRA EL CONTENIDO
```

#### Descargar y subir contenido
```bash
###
rsync <origen> <destino>
###DESCARGAR
rsync rsync://rsync-connect@ip/directorio/fichero.txt <destino>
ej: rsync rsync://rsync-connect@ip/directorio/fichero.txt .

### SUBIR
rsync fichero.txt rsync://rsync-connect@ip/directorio_destino/
```

