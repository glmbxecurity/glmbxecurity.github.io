---
title: "Home Assistant"
layout: single
category: "Proyectos"
slug: "proyectos/home-assistant"
date: 2025-09-30
---

# Home Assistant + IP Camera
En este proyecto se instalará el servicio de Home Assistant para integrar una camara IP en nuestra red.

El acceso será única y exclusivamente a través de una VPN ya previamente configurada.

### Estructura
Red local con:
Ip pública asociada a dyndns:   glmbxecurity.ddns.net  
Home Assistant -> 192.168.1.4 + 10.0.0.6 (wg0)  
Camara IP - > 192.168.1.5  

VPS con:
Ip pública asodiada a dyndns:  glmbxecurity.duckdns.org  
Wireguard server: 194.164.167.198 + 10.0.0.1 (wg0)  
![Estructura_de_red](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/Estructura_red.png)
### Instalación y configuración
Partimos de la base que el servidor wireguard está configurado, y el cliente wireguard de home assistant está conectado a la VPN. Para más detalles de su configuración, mirar mi proyecto de VPN.

#### Preparación Camara
Dependiendo de la cámara se hará de una u otra forma, habrá que mirar en el manual, la idea es habilitar RTSP y/o ONVIF

###### RTSP
Sirve para visualizar la cámara únicamente

##### ONVIF
Sirve tanto para visualizar como para controlar, movimientos de cámara y funciones extra

En nuestro proyecto habilitaremos las 2 en una camara TP-LINK que se suele utilizar con la App "Tapo"

Una vez habilitado, se necesitará anotar las credenciales que se han configurado al habilitar RTSP / ONVIF

#### Instalación Home Assistant
La manera más sencilla es a través de docker, con:
```bash
docker pull homeassistant/home-assistant
```

#### Inicio Home Assistant con el sistema

Crear un fichero docker-compose.yml
```bash
version: "3.9"
services:
  homeassistant:
    container_name: homeassistant
    image: homeassistant/home-assistant
    privileged: true
    restart: unless-stopped
    network_mode: host
    volumes:
      - /home/usuario/homeassistant:/config
    environment:
      - TZ=Europe/Madrid

```

Iniciar contenedor con:
`docker-compose up -d`

Probar a reiniciar a ver si el contenedor aparece iniciado

#### Acceso y configuración
Para acceder a la interfaz de administración, basta con ir a:
```http://10.0.0.6:8123```

Una vez dentro, crearemos nuestro "hogar" y una cuenta de usuario para acceder a home asssistant. Si tenemos un teléfono móvil podemos descargar la APP e iniciar sesión siempre que estemos conectados a la VPN.

##### Configuración camara

En el apartado de configuración de Home Assistant > Integraciones, agregamos una integración y elegimos onvif

Introducimos:
```bash
Nombre: Nombre que le queramos dar
Host: Ip de la cámara (192.168.1.5)
Puerto: 2020
usuario: el configurado al habilitar onvif
contraseña: la que corresponde al usuario
```

### Configurar grabaciones

##### 1. Directorio para almacenar grabaciones
```bash
mkdir -p /root/homeassistant/www/recordings
chmod -R 755 /root/homeassistant/www/recordings

```

#### 2. Montar volumen en docker
Para poder ver los videos e imagenes grabados de la cámara desde la app, tiene que poder ser accesibles desde el docker, para ello montaremos la ruta creada anteriormente en el directorio /media del docker. Esto se hará editando el docker-compose.

Se agrega en volumes la siguiente línea:
```bash
- /root/homeassistant/www/recordings:/media
``` 


##### 3. Configurar Alertas y grabaciones automáticas

Localizar los ID de cámra y sensor en configuración > Dispositovos > Entidades:
* camera.id_camara
* binary_sensor.id_sensor

En mi caso:
* eddygalamba_mainstream
* eddygalamba_cell_motion_detection

##### Automatizaciones y escenas
Una vez localizado estos datos, nos dirigimos a la configuracion del dispositivo y localizamos automatizaciones y escenas.

En automatizaciones > crear una nueva automatización > opción desde cero.

___Después de mucha prueba y error, he dado con la configuración perfecta para mi cámara, no debería ser diferente para la tuya, pero podría cambiar algo.___

Clic en los tres puntos y editar YAML (modificar entity.id, image, action, filename según corresponda)
![automatizacion1](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/automatizacion1.png)

```bash
alias: Alerta de movimiento en cámara
description: Notifica cuando se detecte movimiento y graba un clip de vídeo
triggers:
  - entity_id: binary_sensor.eddygalamba_cell_motion_detection
    from: "off"
    to: "on"
    trigger: state
conditions: []
actions:
  - data:
      title: Alerta de Movimiento
      message: Se detectó movimiento en la cámara.
      data:
        image: http://10.0.0.6:8123/api/camera_proxy/camera.tu_camara
    action: notify.mobile_app_motorola_edge_30_pro
  - target:
      entity_id: camera.eddygalamba_minorstream
    data:
      filename: >-
        /config/www/recordings/movimiento_{{ now().strftime('%Y%m%d-%H%M%S')
        }}.mp4
      duration: 30
    action: camera.record
mode: single
```

**Guardar y reiniciar Home Assistant**

Ahora la cámara debe mandar una alerta a la app del movil motorola, y además ponerse a grabar durante 30 segundos cuando detecte movimiento en el sensor de la cámara.

Luego en ___Medios > My media___ debes de ver las grabaciones
###### Troubleshooting

Si tienes problemas de que no se ve, puedes comprobar que se está accediendo correctamente a los ficheros a través de una URL, y descartar que sea problemas de permisos.

Si el archivo se configura con la ruta `/config/www/recordings/`, los vídeos se almacenarán en tu máquina anfitriona en:

`/home/usuario/homeassistant/www/recordings/`

Se puede  probar a crear un fichero de prueba a ver si accediendo, se ve el fichero:
http://10.0.0.6:8123/local/recordings/prueba.txt


#### 4. Script (cron), limitar grabaciones 1GB

Este script será una tarea cron que se ejecutará a nivel S.O para que el directorio de grabaciones no ocupe más de 1GB, en ese caso eliminará los ficheros más antiguos conforme se vaya "llenando la memoria".

**ejecutamos:**
`crontab -e`

Escribimos abajo del todo:
`*/5 * * * * /root/scripts/limit_card_records_1gb.sh`

Esto ejecutará la tarea cada 5 minutos (se puede editar).

Luego creamos el script y le damos permisos de ejecución. El contenido del script:
```bash
#!/bin/bash

# Carpeta donde se guardan los videos
VIDEO_FOLDER="/root/homeassistant/www/recordings/"

# Límite de espacio en MB (1GB = 1024MB)
LIMIT_MB=1024

# Obtener el tamaño total de la carpeta en MB
current_size=$(du -sm "$VIDEO_FOLDER" | cut -f1)

# Eliminar archivos más antiguos si se supera el límite
while [ "$current_size" -gt "$LIMIT_MB" ]; do
  # Encontrar el archivo más antiguo y eliminarlo
  oldest_file=$(find "$VIDEO_FOLDER" -type f -printf '%T+ %p\n' | sort | head -n 1 | awk '{print $2}')
  rm -f "$oldest_file"
  echo "Eliminado: $oldest_file"

  # Actualizar el tamaño de la carpeta
  current_size=$(du -sm "$VIDEO_FOLDER" | cut -f1)
done
```

# DashBoard Personalizado

Este apartado dependerá del gusto personal y necesidades, pero se puede crear algo así:
![dashboard](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/dashboard.png)

En mi caso puse una preview de la cámara, 3 botones (grabar 30s, tomar imagen y activar/desactivar la alerta+grabación creadas anteriormente).

A continuación un gráfico para monitorizar el movimiento, y un seguimiento de los momentos en que el sensor detecta movimiento.

Para crear el dashboard nos vamos a Configuración > Paneles y creamos uno nuevo (al finalizar, lo podemos establecer como dashboard predeterminado para el dispositivo).

La configuración la hice poco a poco a ensayo y error, pero la configuración final quedaría así (Si quieres algo similar, simplemente puedes copiar y pegar, editando sensores, directorios, etc):
```bash
views:
  - title: Cámara
    sections:
      - type: grid
        cards:
          - type: heading
            heading_style: title
            heading: Cámara Salon
            icon: mdi:camera
          - type: picture-entity
            entity: camera.eddygalamba_minorstream
          - show_name: true
            show_icon: true
            type: button
            tap_action:
              action: perform-action
              perform_action: camera.record
              target:
                entity_id: camera.eddygalamba_minorstream
              data:
                lookback: 0
                filename: >-
                  /config/www/recordings/grabacion_{{
                  now().strftime('%Y%m%d-%H%M%S') }}.mp4
                duration: 30
            entity: camera.eddygalamba_minorstream
            name: Grabar 30s
            grid_options:
              columns: 3
              rows: 2
          - show_name: true
            show_icon: true
            type: button
            tap_action:
              action: perform-action
              perform_action: camera.snapshot
              target:
                entity_id: camera.eddygalamba_minorstream
              data:
                filename: >-
                  /config/www/recordings/imagen_{{
                  now().strftime('%Y%m%d-%H%M%S') }}.jpg
            entity: camera.eddygalamba_minorstream
            name: Tomar foto
            icon: mdi:camera
            show_state: false
            grid_options:
              columns: 3
              rows: 2
          - show_name: true
            show_icon: true
            type: button
            entity: automation.prueba
            show_state: true
            grid_options:
              rows: 2
      - type: grid
        cards:
          - type: heading
            heading_style: title
            heading: Movimientos
          - type: history-graph
            entities:
              - entity: binary_sensor.eddygalamba_cell_motion_detection
            logarithmic_scale: false
          - type: logbook
            target:
              entity_id:
                - binary_sensor.eddygalamba_cell_motion_detection
    badges: []
    background:
      opacity: 33
      alignment: center
      size: cover
      repeat: repeat
      attachment: fixed
      image: /api/image/serve/af189795b7e76a5c378c5360c5ea58cb/original
    cards: []
    type: sections
    max_columns: 4
    icon: mdi:camera
```




