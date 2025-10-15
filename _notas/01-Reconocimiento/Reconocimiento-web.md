---
title: "Reconocimiento Web"
layout: "single"
category: "Reconocimiento"
slug: "reconocimiento/reconocimiento-web"
date: "2025-10-15"
---

### PASIVO
#### Reconocimiento de IP
```bash
host http://sitioweb.com
```

Si nos devuelve 2 direcciones IP (raro), rpobablemente esté detras de un proxy como cloudflare.

#### Robots.txt
En la raíz del sitio web solemos encontrar el robots.txt, que contiene los directorios que no serán indexados, como /wp-admin/. Ejemplo: http:/ip/robots.txt

#### sitemap.xml
Igual que robots.txt nos puede proveer de infornación inicial interesante como autores o directorios de la web que es posible que no descubramos haciendo fuzzing.

#### Wappalyzer y Builtwith
Plugins o addons para identificar las tecnologías utilizadas en el sitio web, asi como detecta plugins de wordpress e información interesante, subdominios y más.

#### Whatweb
Similar a lo anterior pero por línea de comandos.

#### HTTrack
Herramienta descargable para descargar un sitio web de forma completa y poderlo analizar en local, y lo que hace es servirlo por nuyestro puerto 80, solo le debemos pasar la URL y nos montará la web en local. (En ocasiones esta técnica puede no funcionar si se encuentra la web tras un proxy)

#### Whois
Herramienta para el reconocimiento de dominios, donde podemos ver información acerca del dominio, como quien registró el dominio, o la fecha de expiración. Tenemos la herramienta por linea de comandos, o via web en https://who.is
```bash
whois miweb.com
```

#### WaybackMachine
Un sitio web que almacena el estado de cualquier web de internet cada cierto tiempo y nos sirve para ver por ejemplo como era una web hace 6 meses, o hace 14 años, por ejemplo. Puede ser interesante ya que en alguna version antigua de una web podemos detectar información útil para un pentesting.

