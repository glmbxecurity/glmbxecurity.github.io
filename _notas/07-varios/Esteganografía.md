---
title: "Esteganografía"
layout: "single"
category: "Varios"
slug: "varios/esteganograf-a"
date: "2025-09-30"
---

### Strings

El comando strings sirve para mostrar cadenas de texto legíbles, ocultas dentro de ficheros binarios que a priori no son legibles, como una imagen. En ocasiones, la máquina nos dirige hacia una imagen o fichero que en principio no parece ser nada, pero que igual oculta algún mensaje importante.
```bash
strings <ichero>
```

### steghide
Es posible analizar algun fichero en busca de datos ocultos, para ello buscamos a ciegas con este comando.
``` bash
steghide extract -sf fichero_a_analizar -xf datos_ocultos_a_extraer.txt
#Si nos pide contraseña lo dejamos en blanco

#Luego con el comando file sacamos el tipo de fichero

file datos_ocultos_a_extraer.txt
```
