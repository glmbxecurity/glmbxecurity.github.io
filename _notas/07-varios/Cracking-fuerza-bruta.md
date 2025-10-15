---
title: "Cracking Fuerza Bruta"
layout: "single"
category: "Varios"
slug: "varios/cracking-fuerza-bruta"
date: "2025-09-30"
---

#### IMPORTANTE AL USAR JOHN
Al crackear hashes a veces no nos muestra en la salida del programa la clave, para verla basta con ejecutar:
```bash
john --show <nombre_del_fichero_crackeado>

#EJEMPLO
john --show hash
```
### Cracking ZIP
#### Con FcrackZIP

```bash
fcrackzip -v -u -D -p <diccionario> <fichero.zip>
```
#### Con John the ripper

```bash
# Primero extraemos el hash del zip
zip2john fichero.zip > hash_del_zip

# Segundo ataque de fuerza bruta contra ese hash
john --wordlist=<diccionario> hash_del_zip
```

### Cracking Keepass database
#### Con john the ripper
```bash
# Convertimos la database.kdbx para crackear con john
keepass2john Database.kdbx > hash

# Crackeamos con john
john --w
```

### Cracking /etc/shadow
el cracking de /etc/shadow se realiza en 2 fases, y para ello necesitaremos los ficheros passwd y shadow. 

TENIENDO:
```bash
Necesitamos la linea del passwd y del shadow en un fichero cada uno, del usuario a crackear, ej:

# shadow.txt
root:$6$riekpK4m$uBdaAyK0j9WfMzvcSKYVfyEHGtBfnfpiVbYbzbVmfbneEbo0wSijW1GQussvJSk8X1M56kzgGj8f7DFN1h4dy1:18226:0:99999:7:::

# passwd.txt
root:x:0:0:root:/root:/bin/bash
```

PRIMERO
```bash
unshadow passwd.txt shadow.txt > unshadowed.txt
```

SEGUNDO
```bash
john --wordlist="diccionario" unshadowed.txt
```

### Cracking ficheros GPG cifrados
Teniendo un fichero **.pgp** y su clave **.asc** se puede descifrar el fichero, pero el proceso suele requerir de la "clave/passphrase" para el .asc. Para ello se puede crackear con john the ripper y luego descifrar el fichero.

1º convertir la clave.asc en un fichero hash entendible para john
```bash
gpg2john clave.asc hash
```

2º crackear el hash
```bash
john hash --wordlist=/usr/share/wordlists/rockyou.txt
```

3º importar la clave
```bash
gpg --import clave.asc
```

4º desencriptar el fichero gpg con la clave.asc y el "pasphrase" obtenido anteriormente con john
```bash
gpg --decrypt fichero.gpg clave.asc
```



