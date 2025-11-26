---
title: "Hash Cracking & Wordlists (JtR)"
layout: "single"
category: "Criptografia"
slug: "criptografia/hash-cracking"
date: "2025-11-26"
---

### 1. Generar Diccionarios (Wordlists)

**CUPP (Perfilado de usuario):**
Crea diccionarios basados en datos personales (mascotas, fechas).
```bash
cupp -i
```

**CeWL (Spidering Web):**
Crea un diccionario con las palabras que aparecen en una web.
```bash
cewl http://target.com -w target_wordlist.txt
```

---

### 2. John The Ripper (JtR)

**Ver contraseñas ya crackeadas:**
```bash
john --show hash.txt
```



**Cracking Linux (/etc/shadow):**
Necesitas `passwd` y `shadow`.
```bash
# 1. Unificar
unshadow passwd.txt shadow.txt > unshadowed.txt

# 2. Crackear
john --wordlist=/usr/share/wordlists/rockyou.txt unshadowed.txt
```

**Cracking ZIP:**
```bash
# 1. Extraer hash
zip2john fichero.zip > hash_zip.txt

# 2. Crackear
john --wordlist=rockyou.txt hash_zip.txt
# (Alternativa antigua: fcrackzip -v -u -D -p rockyou.txt fichero.zip)
```

**Cracking Keepass (.kdbx):**
```bash
keepass2john Database.kdbx > hash_keepass.txt
john --wordlist=rockyou.txt hash_keepass.txt
```

**Cracking SSH (id_rsa):**
```bash
ssh2john id_rsa > hash_ssh.txt
john --wordlist=rockyou.txt hash_ssh.txt
```

**Cracking GPG (.asc):**
```bash
# 1. Extraer hash
gpg2john clave.asc > hash_gpg.txt

# 2. Crackear
john --wordlist=rockyou.txt hash_gpg.txt

# 3. Importar y Descrifrar
gpg --import clave.asc
gpg --decrypt fichero.gpg
```

**Cracking Hashes MD5/SHA Online:**
* [CrackStation](https://crackstation.net)
* [Hashes.com](https://hashes.com)
