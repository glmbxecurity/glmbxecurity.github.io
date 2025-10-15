---
title: "Repositorio Git"
layout: "single"
category: "Varios"
slug: "varios/repositorio-git"
date: "2025-09-30"
---

En algunas webs, nos podemos encontrar al realizar el reconocimiento, que nmap nos reporta la existencia de un repositorio de git. y además nos indica la ruta.


### Dumpear repositorio git
En este momento, podemos dumpear el repositorio a nuestra máquina con herramientas como **git-dumptool**. Hay muchas de este tipo.

### Analizar la información
* con ```git log```, podemos ver los comits.
* con ```git show```, seguido de los primeros digitos del commit, podemos ver los cambios en el código.

Podriamos ver información interesante como crecenciales o similares, o comentarios que nos pueden animar a ver un diff.

### Ver contenido de diffs
Si en algún diff se menciona algo como, inserción, o eliminación de información sensible como pueden ser contraseñas:
```bash
git diff <el codigo largo del diff>

#ejemplo
git diff a4d900a8d85e8938d3601f3cef113ee293028e10
```

