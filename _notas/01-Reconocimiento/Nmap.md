---
title: "Nmap"
layout: "single"
category: "Reconocimiento"
slug: "reconocimiento/nmap"
date: "2025-09-30"
---

```bash 
nmap <ip> <parametros>
``` 

### Escaneo básico Nmap 

```bash
# Primer escaneo simple para conocer puertos abiertos
nmap 10.10.10.4 -p- --open -n -Pn --min-rate 2000 -oG fichero.txt
nmap 10.10.10.4 --top-ports 10000 --open -n -Pn --min-rate 2000 -oG fichero.txt

# Escaneo a puertos UDP (en ocasiones hay servicios corriendo en un puerto UDP)
nmap 10.10.10.4 -sU --top-ports 200 --min-rate 2000 -Pn -oG fichero.txt

# Escaneo conociendo los puertos abiertos
nmap 10.10.10.4 -p 22,80,445 -n -Pn --min-rate 2000 -sS -sCV -oG fichero.txt
```

### Escaneo Nmap como un PRO

Primero realizamos un escaneo básico y extraemos todos los puertos:
```bash
nmap -p- <IP> >nmap.txt

cat nmap.txt | tr '/' ' ' | grep "^[0-9]" | awk '{print $1}' | tr '\n' ',' | sed 's/,$/\n/' > nmap
```

Ahora con todos los puertos obtenidos y separados por comas, podemos copiar ese texto y realizar un escaneo potente:

```bash
nmap 10.10.10.4 -p 22,80,445 -n -Pn --min-rate 2000 -sS -sCV -oG fichero.txt
```

### Scripts Nmap
```bash
# Con la opción -sC utiliza el script por defecto para encontrar vulnerabilidades, si queremos utilizar un script específico, podemos consultar el listado de scripts

ls /usr/share/nmap/scripts

# Elegir el script deseado y realizar el escaneo de la siguiente manera
nmap 10.10.10.4 --script "vuln" -p 445
``` 

### Detección Firewall
Con el parámetro -sA podremos tratar de detectar si hay algun firewall. Si en el escaneo aparece **unfiltered** es que no hay firewall, por el contrario si aparece **filtered** podemos asegurar que hay algun tipo de cortafuegos.
```bash
nmap -Pn -sA 10.10.10.1
```
### Evasion de Firewall / IDS con Nmap
Se puede intentar evitar el bloqueo por parte del firewall al intento de escaneo de puertos. para ello algo muy común es el hecho de fragmentar los paquetes, o indicar el tamaño maáximo de MTU (tamaño mínimo de transimision de unidad), o falsear ciertos datos.  

#### Fragmentando paquetes
```bash
nmap -Pn -sS -f 10.10.10.10
```

#### Estableciendo MTU personalizada
```bash
nmap -Pn -sS --mtu 8 10.10.10.10
```

#### Spoofing 
```bash
nmap -Pn -sS 10.10.10.10 -D 192.168.1.1 -g 443 --spoof-mac AA:BB:CC:DD:EE:FF
```

#### Cambiando TTL y data-length
```bash
nmap -Pn -sS -f 10.10.10.10 --data-length 200 --ttl 127
```
   