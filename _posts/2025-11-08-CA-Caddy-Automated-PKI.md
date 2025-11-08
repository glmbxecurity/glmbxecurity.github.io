---
layout: single
title: Smallstep + Caddy ACME Automated Certs
date: 2025-09-30
categories:
  - projects
author: Edward Herrera Galamba
excerpt: Smallstep CA y Caddy | Certificados automaticos con ACME
---
## Smallstep ACME server + Caddy

### Configuraciones iniciales y consideraciones
Para poder realizar solicitudes via ACME, debemos tener un DNS funcional y con las entradas DNS antes de solicitar el certificado.  

Al menos debemos tener: 
* entrada DNS de la CA (ej: ca.glmbx.home)
* Entrada DNS del servicio a certificar (apuntando nombre a la maquina donde está alojado el servicio / web)(en caso de usar caddy tiene que apuntar a caddy)
* Si usamos caddy, deben estar en lxc o vm distintas, ya que ambas usan el 80 y el 443, modificar esto complica aún mas el lab

La solicitud ACME debe ser realizada desde el equipo el cual se quiere certificar, para que el challenge pueda verificar que, el nombre asociado a la IP, es el mismo que está solicitando y tiene levantado el puerto 80 para resolver el challenge (en caso de http-01 challenge, que es el default). (salvo si usamos caddy, que debe apuntar a caddy)

### Instalar e iniciar CA
#### Instalar en Alpine linux
```bash
apk update && apk upgrade
apk add step-cli step-certificates ca-certificates
```

#### Iniciar CA
Lanzamos el comando y rellenamos la info:  
  
```bash
~ # step ca init
✔ Deployment Type: Standalone
What would you like to name your new PKI?
✔ (e.g. Smallstep): Glmbx Home CA
✔ (e.g. ca.example.com[,10.1.2.3,etc.]): ca.glmbx.home
What IP and port will your new CA bind to? (:443 will bind to 0.0.0.0:443)
✔ (e.g. :443 or 127.0.0.1:443): :443
What would you like to name the CA's first provisioner?
✔ (e.g. you@smallstep.com): eddygalamba@glmbx.home

```  
Importar los certificados root e intermediate_ca al s.o:
 
```bash
apk add ca-certificates
cp .step/certs/* /usr/local/share/ca-certificates/
update-ca-certificates

# Iniciar por primera vez la CA
step-ca .step/config/ca.json
```
#### Agregar Provisioner ACME 
```bash
step ca provisioner add acme-glmbx-home --type ACME
```

### Prueba ACME
#### Ejemplo certificar Adguard
Desde adguard con step-cli instalado, teniendo los certificados root e intermediate importados(arriba se explica como), y la entrada DNS correctamente registrada (este caso asociando adguard.glmbx.home a la 192.168.1.102):

```bash
step ca certificate adguard.glmbx.home adguard.crt adguard.key --acme https://ca.glmbx.home:443/acme/acme-glmbx-home/directory
```

### Caddy Proxy Server + ACME
En este apartado no se explica como instalar caddy, directamente vamos a la configuracion, para usar Caddy como proxy inverso, y automatizar la solicitud y renovacion de certificados automaticamente.


### Certificado accesible para caddy
Debemos descargar el root_ca.crt de la CA y pasarlo a Caddy
```bash
mkdir -p /etc/ssl/step
cp ./root_ca.crt /etc/ssl/step/
chown caddy:caddy /etc/ssl/step/root_ca.crt
chmod 644 /etc/ssl/step/root_ca.crt
```
#### Caddyfile
El caddyfile es donde agergaremos las entradas para nuestros sitios web

```bash
# /etc/caddy/Caddyfile
{
    email eddygalamba@glmbx.home
    acme_ca https://ca.glmbx.home:443/acme/acme-glmbx-home/directory
    acme_ca_root /etc/ssl/step/root_ca.crt
    http_port 80
    https_port 443
}

adguard.glmbx.home {
    reverse_proxy 192.168.1.102:80
}

cloud.glmbx.home {
    reverse_proxy 192.168.1.103:80
}

```

### Lanzar Caddy
Para lanzar por primera vez y ver el output, detectar posibles problemas:
```bash
caddy run --config /etc/caddy/Caddyfile --adapter caddyfile
```


### Iniciar servicios automaticamente
#### Step CA
Creamos el fichero **/etc/step-ca/password.txt** con la clave que pusimos al crear la CA

```bash
touch /etc/step-ca/password.txt
echo "Micontraseña" > /etc/step-ca/password.txt
```

Creamos el fichero de servicio **/etc/init.d/step-ca**, si existe, lo sobreescribimos con el siguiente contenido:

```bash
#!/sbin/openrc-run

description="Smallstep Certificate Authority"

command="/usr/bin/step-ca"
command_args="/root/.step/config/ca.json --password-file /etc/step-ca/password.txt"
command_background="yes"
pidfile="/run/step-ca.pid"
name="step-ca"
command_user="root:root"
depend() {
    need net
}

start_pre() {
    checkpath --directory /var/log/step-ca --mode 0755
}

start() {
    ebegin "Starting Step CA"
    start-stop-daemon --start --quiet \
        --background \
        --make-pidfile \
        --pidfile "${pidfile}" \
        --exec ${command} -- ${command_args}
    eend $?
}

stop() {
    ebegin "Stopping Step CA"
    start-stop-daemon --stop --quiet --pidfile "${pidfile}"
    eend $?
}

```

Iniciamos y lo establecemos al inicio
```bash
rc-update add step-ca default
rc-service start step-ca
```
### Caddy
Creamos el fichero **/etc/init.d/caddy** (o sobreescribimos su contenido) con:

```bash
#!/sbin/openrc-run

/etc/init.d # cat caddy 
#!/sbin/openrc-run

description="Caddy Web Server"

command="/usr/sbin/caddy"
command_args="run --config /etc/caddy/Caddyfile --adapter caddyfile"
command_background="yes"
pidfile="/run/caddy.pid"
name="caddy"

depend() {
    need net
    use dns logger
}

start_pre() {
    checkpath --directory /var/log/caddy --mode 0755
}

start() {
    ebegin "Starting Caddy"
    start-stop-daemon --start --quiet \
        --background \
        --make-pidfile \
        --pidfile "${pidfile}" \
        --exec ${command} -- ${command_args}
    eend $?
}

stop() {
    ebegin "Stopping Caddy"
    start-stop-daemon --stop --quiet --pidfile "${pidfile}"
    eend $?
}

```

Iniciamos y lo establecemos al inicio
```bash
rc-update add caddy default
rc-service start caddy
```












