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
mkdir <nombre_repositorio>
cd !$
git init --bare
git config --global user.mail "tu_email"
git config --global user.name "Nombre.apellidos"
```

Si queremos usar mi plantilla, clonamos mi repositorio, se elimina el contenido del directorio content, y se edita la plantilla para personalizarla. (en content es donde irán los post.). sino, puedes buscar una plantilla por internet que te guste.
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
themes/hugo-book/assets

```

Para lanzar la web, nos posicionamos en el directorio del repositorio y ejecutamos:
```bash
hugo server --bind <ip_del_servidor> -p 80
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
git clone usuario@ip:/ruta_al_repo/
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


