### Con FcrackZIP

```bash
fcrackzip -v -u -D -p <diccionario> <fichero.zip>
```
### Con John the ripper

```bash
# Primero extraemos el hash del zip
zip2john fichero.zip > hash_del_zip

# Segundo ataque de fuerza bruta contra ese hash
john --wordlist=<diccionario> hash_del_zip
```