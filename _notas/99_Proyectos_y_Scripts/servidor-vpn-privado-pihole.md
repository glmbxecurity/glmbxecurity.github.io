---
title: Servidor Vpn Privado + Pihole
layout: single
category: Proyectos
slug: proyectos/servidor-vpn-privado-pihole
date: 2025-09-30
---

# Servidor VPN privado + PiHole

### Introducción
Este proyecto trata de montar tu propio servidor de VPN, válido tanto para montar en casa con un viejo equipo, raspberry o dispositivo similar, como para montar en un VPS (Que es mi caso, y es la mejor opción).

### Apertura de puertos
Tanto si se trata de un VPS como si se monta en casa, habrá que abrir el puerto en el router / firewall para la comunicación con el servicio de VPN en este caso **wireguard**, cuyo puerto por defecto es el **51820**. En caso de que durante la instalación se elija otro, se deberá abrir dicho puerto.

### Instalacion PiHole
Para blouear publicidad, telemetría, seguimiento, etc, utilizaremos PiHole, que es básicamente un servicio DNS que bloquea una enorme cantidad de DNS maliciosos y no deseados. Es importante primero instalar pihole y luego wireguard para que la configuración sea mas sencilla, ya que luego wireguard detectará pihole y será más comodo de configurar. Introducimos el siguiente comando:

```bash
apt update
curl -sSL https://install.pi-hole.net | bash
```

Comienza la instalación, nos irá haciendo preguntas:
* Interfaz en la que estará a la escucha: **la que tengamos o nos interese**
*  Upstream provider: **el que queramos** (mas adelante se pueden agregar upstream servers)
*  Third party blocklist: **YES**
* Install admin web interface: **YES**
* Install lighthttpd and required php modules: **YES**
* Enable query logging: Recomendado **YES**
* PRivacy mode for FTL: Esto hace referencia a que queremos que se vea al consultar la web, si todo, esconder los dominios, esconder clientes, modo anónimo. (Si es la primera vez, se recomienda **show everything** para comprobar el funcionamiento).

Ahora cambiaremos la contraseña por defecto de acceso a pi-hole:
```bash
pihole -a -p
```

Para acceder:
```bash
http://ip/admin
```

#### Consideraciones
Conviene explorar todas las posibilidades que tiene, se puede elegir quien queremos que pueda hacer peticiones, establecer un DHCP, consultar dominios bloqueados, clientes, logs, etc.

### Instalación Wireguard
Haremos uso de PiVPN, ya que hace una instalación super sencilla, ahorrando todos los pasos engorrosos de la instalación y configuración de wireguard.

```bash
curl -L https://install.pivpn.io | bash
```

Automáticamente comienza la instalación, nos hará algunas preguntas iniciales, luego las preguntas importantes:
* Servidor de vpn - **wireguard**
* puerto - **51820**
* Detecta Pihole, nos pregunta si queremos usar Pi-hole como nuestro DNS para la VPN: **yes**
* Usar IP pública o entrada DNS:  **lo que mas interese**. (se puede hacer uso de DNS dinámicos en caso de hacer la instalación en casa, o tirar de **duckdns.org** o similares en caso de VPS ).

Se generarán las claves, preguntará si queremos actualizaciones desatendidas: **yes** y reiniciar. Ya está listo para su uso.

#### Creación de clientes
Para crear un cliente:
```bash
pivpn -a
```

Consultar el fichero de configuración de un cliente específico
```bash
cat /etc/wireguard/configs/cliente1.conf
```

generar qr de un cliente:
```bash
pivpn -qr
```

#### Conectar un cliente
Para conectar un cliente basta con descargar el programa cliente, añadir un túnel y pegar la configuracion.conf generada anteriormente, o escanear el qr.

En caso de realizar una configuración manual, necesitaremos consultar los datos en **/etc/wireguard/configs/**

### Recomendaciones finales
Se recomienda no tener expuesto ninfún puerto al exterior que no sea el de wireguard, si queremos tener ssh, o acceder al pi-hole web admin interface, mejor hacerlo estando conectado a la VPN y evitar una exposición de servicios de forma innecesaria.



