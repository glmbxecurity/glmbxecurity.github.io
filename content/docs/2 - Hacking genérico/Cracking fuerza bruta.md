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