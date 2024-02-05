
### Con john the ripper
```bash
# Convertimos la database.kdbx para crackear con john
keepass2john Database.kdbx > hash

# Crackeamos con john
john --wordlist=<diccionario> hash
```