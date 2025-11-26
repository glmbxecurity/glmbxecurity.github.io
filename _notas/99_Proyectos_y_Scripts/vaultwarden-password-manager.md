---
title: "Vaultwarden Password Manager"
layout: single
category: "Proyectos"
slug: "proyectos/vaultwarden-password-manager"
date: 2025-09-30
---

# Instalacion gestor de contraseñas Vaultwarden
## Pre-requisitos
```bash
apt update
apt install docker.io
apt install docker-compose
```
### Vaultwarden
Creamos un directorio para los contenedores, uno para vaultwarden y otro para nginx-proxy-manager
```bash
git clone https://github.com/jmlcas/vaultwarden
cd vaultwarden
dockerp-compuse up -d
```
Datos por defecto en la instalacion:
* localhost:8200


### Nginx-Proxy-Manager
```bash
git clone https://github.com7jmlcas/nginx-proxy-manager
cd nginx-proxy-manager
docker-compose up -d
```
Datos por defecto en la instalacion:
* localhost:81
* admin@example.com:changeme

## Configuracion Nginx Proxy
Primeramente cambiamos el email y pass por defecto.
Luego en hosts->New proxy host:
```bash
Forward hostname/IP: la ip de la maquina
Forward port: 8200
Domain names: el nombre que le daremos al DNS y que hará el forward, ej: vaultwarden.et.ms.esp
```

## Certificar servidor
Generar un certificado tipo web:
```bash
step ca certificate vaultwarden.et.ms.esp vaultwarden.crt vaultwarden.key
```

Para importar, en nginxproxymanager, nos vamos a SSL Certificates --> Add SSL Certificate --> Custom
Una vez importado en Hosts --> Editamos y en la pestaña SSL elegimos el certificado generado anteriormente.

## Configuraciones EXTRA
Vaultwarden tiene 2 maneras de configurarse: Mediante las variables de entorno o mediante el fichero config.json. Es recomendable no mezclar ambas opciones, ya que la segunda sobreescribirá a la primera. Dicho fichero de configuración se genera la primera vez que arrancamos el contenedor a partir de la configuración de las variables de entorno, por lo que recomiendo definirla ahí y, una vez arrancado, eliminar del docker-compose.yml aquella configuración que no necesitemos ya o que sea más sensible (como los token). Para una configuración básica pero completa, he utilizado la siguiente (puedes consultar todas las posibles configuraciones en la wiki del proyecto).

Las variables de entorno se editan en el docker-compose file, y debe tener una pinta algo así:
```bash

version: "3.3"

services:

  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    volumes:
      - ./vaultwarden:/data/
    ports:
      - 8200:80
    restart: unless-stopped
    environment:
    - ADMIN_TOKEN='el token de admin'


```


```
* LOG_FILE: Define el nombre del fichero de log que usará el servicio. La ruta hace referencia dentro del contenedor.
* LOG_LEVEL: Definimos el nivel de log, desde trace a error, pudiendo deshabilitar el log poniendo el nivel a off.
* EXTENDED_LOGGING: Combinado con el anterior, nos permite definir el nivel de log.
* DOMAIN: Lo usaremos para poner el dominio de nuestro servicio, y será necesario tanto para el envío de correos como para el acceso web. En el ejemplo, exponemos el servicio en https://bitwarden.midomin.io
* SIGNUPS_ALLOWED: Con esta variable, permitimos o denegamos que cualquiera se pueda dar de alta en nuestro servicio. Deberá estar a true la primera vez, para que, por lo menos, podamos crear nuestra cuenta, y después lo cambiaremos a false ¡o cualquiera podría registrarse en nuestro servicio y utilizarlo!
* INVITATIONS_ALLOWED: Si esta variable está a true, permitiremos que, aquellas cuentas que hayan recibido un enlace de invitación de nuestro servicio, se puedan registrar aunque tengamos prohibido el registro con la variable SIGNUPS_ALLOWED=false.
* ADMIN_TOKEN: Si esta variable está definida, se nos habilitará el endpoint /admin, el cual nos permitirá gestionar nuestro servicio, usuarios, organizaciones, etc. El valor que pongamos será el que nos pedirá para acceder a dicha administración, por lo que, si deseamos tener habilitado el acceso, recomiendo poner un valor generado complicado de conocer, haciendo uso, por ejemplo, del comando openssl rand -base64 48 en cualquier terminal.
* PRECAUCIÓN: Mantén el token especificado en ADMIN_TOKEN a salvo y a buen recaudo, es ni más ni menos que la contraseña de acceso a la zona de administración de tu servidor de contraseñas.
```

# Habilitar panel de admin
El panel de administración se encuentra deshabilitado por defecto, pero se puede habilitar añadiendo la variable **ADMIN_TOKEN** al docker compose file. Primero se debe generar con el siguiente comando:
```bash
openssl rand -base64 48

```

Luego añadimos el token al fichero de docker compose y debemos duplicar cada "$" que nos encontremos, para evitar la interpolación de variables.
finalmente:
```bash
# Tiramos
sudo docker compose -f /home/administrator/vaultwarden/docker-compose.yaml down vaultwarden

#Levantamos
sudo docker-compose -f /home/administrator/vaultwarden/docker-compose.yaml up vaultwarden

# Ojo con la ruta del fichero
```
Ahora ya accedemos al portal admin http://vaultwarden.et.ms.esp/admin
IMPORTANTE: para loguear hay que meter el token con las comillas, sino no entrará jamás.

#### EXTRA
Para facilitar el habilitado / deshabilitado del panel, se hace una copia del docker-compose con el admin habilitado, y se utiliza cuando se quiera habilitar.
