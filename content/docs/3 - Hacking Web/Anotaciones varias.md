### Cuando en una web hay un admin que revisa links, mensajes, etc

Cuando en una web, vemos algún mensaje o texto que nos indique o nos insinúe que alguien comprobará nuestro link o un mensaje (por ejemplo si hay un chat), esto se puede prestar para un **CSRF**, un **XSS** para obtener cookies de sesión o para montar un **Phishing** con la vulnerabilidad de [[Vulnerabilidad Target blank]], por ejemplo.

### Fichero info.php

Cuando encontramos el fichero info.php (fichero de configuración de php), en ocasiones podemos enumerar algún usuario que esté incluído en el fichero. en **Configuration > Apache2handler > User/Group** 

### Id=1
Cuando tenemos una url en la que se dirige a un perfil, un producto, etc, de la siguiente manera: ```http://ip/product=2```, o ```http://ip/pofile.php&id=1```


