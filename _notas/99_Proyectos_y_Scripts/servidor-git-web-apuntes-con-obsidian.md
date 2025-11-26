---
title: "Servidor Git + Web Apuntes Con Obsidian"
layout: single
category: "Proyectos"
slug: "proyectos/servidor-git-web-apuntes-con-obsidian"
date: 2025-09-30
---

# Servidor GIT + Web apuntes con obsidian
En este proyecto  se montará un servidor de git y un portal web con nginx, el contenido de la documentación se editará mediante obsidian. Además se explicará como subirlo a github y tener tu propia github page.

### Servidor git
Instalacion y creacion repositorio. Crearemos el usuario git, y meteremos las authorized heys de los colaboradores del servidor.
```bash
apt update
apt install tmux (si no lo tienes, es recomendable)
sudo adduser git
su git
cd
mkdir .ssh && chmod 700 .ssh
touch .ssh/authorized_keys && chmod 600 .ssh/authorized_keys
apt install git
mkdir <nombre_repositorio.git>
cd !$
git init --bare
git config --global user.mail "tu_email"
git config --global user.name "Nombre.apellidos"
```

Si queremos usar mi plantilla, clonamos mi repositorio, se elimina el contenido del directorio content y todo lo relacionado con git, y se edita la plantilla para personalizarla. (en content es donde irán los post.). sino, puedes buscar una plantilla por internet que te guste.
```bash
git clone 'https://github.com/glmbxecurity/glmbxecurity.github.io'
cd glmbxecurity.github.io
```
### Autorizacion de usuarios

En cada usuario que queramos autorizar, generamos un par de claves ssh
```bash
ssh-keygen -t rsa
```

En el servidor git, metemos la clave publica del usuario/editor en authorized keys
```bash
cat /id_rsa.pub >> /home/git/.ssh/authorized_keys
```

### Primera inicializacion
El directorio creado en el servidor donde se inicializó, no es el directorio de trabajo donde estará el contenido, sino es un directorio sobre el que trabaja el servidor para controlar los cambios. Como queremos montar un servidor web, debemos de clonar el repositorio a un directorio diferente (que este sí contendrá los ficheros de la web).

```bash
mkdir documentacion_server
git clone git@ip:/ruta_al_repositorio.git>
git add *
git commit -m "primera inicializacion"
git push origin master
```
### Montar y editar la web
Instalamos pre-requisitos
```bash
apt install golang
apt install hugo
```

Editamos la web, la estructura de la web está de la siguiente manera:
```bash
# Posts e index
- Directorio content y content/docs

# Fichero configuracion principal (hay que editar la ruta de content)
- config.toml

#Editar titulo de la pagina
_index.md

#Favicon
static/favicon

# CSS
themes/hugo-book/assets/_main.scss

# Color de titulos
themes/hugo-book/assets/_custom.scss

```

Para lanzar la web, nos posicionamos en el directorio del repositorio y ejecutamos:
```bash
hugo server --bind <ip_del_servidor>
```

### Editar la web (Colaboradores)

#### Si es la primera vez
Previamente la id_rsa.pub enviada al adminstrador del sitio, teniendo git y obsidian instalado, lo primero clonamos el repositorio:
```bash
# Configurar tu cliente git
git config --global user.mail "tu_email"
git config --global user.name "Nombre.apellidos"

#Si está el repo en internet
git clone https://ruta_al_repo.git

# Si es alojado en una organizacion
git clone git@ip:/ruta_al_repo.git/
```

Abrimos obsidian y editamos la web. Si es la primera vez:
```bash
"Open folder as a vault" > elegir el directorio content/docs del repositorio
```

Subir los cambios
```bash
#Posicionado en la raíz del repositorio
git add *
git commit -m "Comentario resumen de los cambios"
git push origin master
```

#### Si no es la primera vez
```bash
* git pull origin master
* editar
* git add *
* git commit -m "Comentario"
* git push origin master
```

### Hosteo web con NGINX

#### Importante tener en cuenta
Al lanzar el comando **hugo** en la raíz del repositorio, se construye la web e el directorio **public**. Esto es importante saberlo, ya que si realizamos cambios y no tenemos hugo corriendo, habrá que lanzarlo para que se actualize el directorio public con los nuevos cambios. De lo contrario nunca veremos nuestra web actualizada.


Instalar servicio, y crear un fichero de configuracion del sitio, partiendo del default.
```bash
apt install nginx
cd /etc/nginx/sites-available
cp default documentacion_server
ln -s /etc/nginx/sites-available/documentacion_server /etc/nginx/sites-enabled/documentacion_server
vim mysite
```

La configuración tendrá la siguiente pinta:
```bash
server { 
	listen 80; 
	listen [::]:80; 
	
	server_name mysite.com www.mysite.com; 
	root /var/www/documentacion_server/public; 
	index index.html; 
	
	location / { 
		try_files $uri $uri/ =404; 
	} 
}
```

Ya que tenemos la "web" en un repositorio en algun lugar del servior, deberemos enlazar este repositorio con el lugar donde dijimos a nginx que debía leer los ficheros web.
```bash
ln -s /documentacion_server /var/www/documentacion_server
```

Para comprobar la configuracion
```bash
service nginx configtest
```

Lanzar y parar el servicio
```bash
systemctl start nginx
systemctl stop nginx
```

#### IMPORTANTE
Cada vez que se realicen modificaciones/cambios en la web, para que se vea reflejado en nginx, hay lanzar el comando **hugo** en la raíz del repositorio.

Cuando se crean ficheros desde el colaborador, cambia el propietario, hay que cambiar el propietario para poder lanzar **hugo**.
```bash
chown -R git:git *
hugo
```

### Hosteo en Github Pages (Pdte desarrollo)



