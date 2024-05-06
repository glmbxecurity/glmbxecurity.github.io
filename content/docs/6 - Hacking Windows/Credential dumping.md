### Ficheros de configuracion
Cuando se realiza una instalación masiva desatendida, las claves se suelen almacenar (a veces en base64), en los siguientes ficheros:
 ```bash
  C:\\Windows\Panther\Unattend.xml
  C:\\Windows\Panther\Autounattend.xml

### AL FINAL DEL FICHERO ENCONTRAMOS
<AutoLogon>
	<Password>
		<value>CONTRASEÑA</value>
```

Esto puede ser interesante porque la contraseña que se suele almacenar es la del administrador, de cara a la escalada de privilegios.

 