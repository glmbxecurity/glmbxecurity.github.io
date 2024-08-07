### Socat (EL MAS INTERESANTE)
Viene preinstalado con linux, es muy interesante, ya que una vez obtenido el acceso a la máquina, si queremos exponer un puerto que antes no lo estaba, por ejemplo el 8080 (solo expuesto para la 127.0.0.1). 
De esta manera, directamente estamos exponiendo un puerto con la ip de la víctima que antes no estaba.

*Con otras herramientas lo enviaríamos el puerto al "localhost" del atacante. *

##### EJEMPLO PRÁCTICO
En la víctima está el servicio librenms con el puerto 8080 que solo se puede acceder desde el localhost de la víctima. Hay un exploit para librenms y necesito exponer ese puerto para poderlo explotar.

```bash
### EL PUERTO 8080 QUE SOLO ESTABA EXPUESTO LOCALMENTE, AHORA TAMBIÉN SE VERÁ POR EL PUERTO 5000 QUE ESCUCHARÁ PETICIONES DESDE FUERA DEL "LOCALHOST"
socat TCP-LISTEN:5000,fork,reuseaddr tcp:127.0.0.1:8080

bastaría con acceder a la url http://<ip_victima>:5000
 ```

### Chisel

En el atacante:
```bash
chisel server --reverse -p <puerto_escucha>
```

en la víctima:
```bash
chisel client <ip_atacante>:<puerto_escucha_del_atacante> R:<puerto_que_queremos_exponer>
```

**Si estamos por ejemplo queriendo exponer el 3306 de la víctima, y estamos a la escucha por el 1234 del atacante, realmente se nos está enviando el 3306 al atacante**

### Con SSH
Cuando tenemos acceso a una máquina, hay servicios que por algun motivo solo están corriendo para el "localhost". A veces nos interesa acceder a ese servicio ya que puede ser un panel web de administración, por ejemplo.

Supongamos una máquina que corre un servicio web en el puerto 9999 y lo queremos ver desde nuestro equipo en el puerto 8080.

```bash
ssh usuario@ip -L 8080:localhost:9999

# -L especifica redirección de puertos y funciona así
# local_port:remote_host:remote_port


```

Ahora basta con dirigirnos al navegador web de nuestra máquina atacante y dirigirnos a la URL **http://localhost:8080**

**Para Simplificar lo mejor es que tanto el puerto local como el remoto sean iguales, pero no siempre se podrá, porque puede que tengamos ese puerto ocupado**

### Metasploit portfwd
```bash
portfwd add -l [puerto_local] -p [puerto_remoto] -r [IP_remota]
```





