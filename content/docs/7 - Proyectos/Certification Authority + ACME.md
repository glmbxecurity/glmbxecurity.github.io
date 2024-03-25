# Entidad Certificadora con Auto-enrollment

### Que es una CA?
Una autoridad confiable responsable de emitir certificados digitales. Estos certificados son utilizados para autenticar la identidad de entidades en línea, como sitios web, aplicaciones o usuarios. La función principal de una CA es garantizar la integridad y autenticidad de la información intercambiada a través de Internet mediante el uso de criptografía de clave pública.

### Como funciona?
La CA emite un certificado para un servicio, los clientes tienen importado el certificado de la CA Raíz (ya sea de forma manual o por políticas de dominio). Estos clientes al visitar, por ejemplo un sitio web certificado por la CA, confían en este certificado ya que ha sido emitido por una CA confiable.

El Auto-enrollment, sirve para renovar este certificado cada cierto tiempo de manera automática, por ejemplo 24h, de manera que si ha sido vulnerado de alguna forma el certificado, este no sería válido pasadas las 24h de su emisión, y el servicio solicitaría un nuevo certificado confiable.

### Laboratorio CA + ACME
En este laboratorio instalaremos una CA standalone, en un dominio ficticio de empresa privada y certificaremos de manera automática un servidor web IIS,  con renovación automática del certificado cada 24h. Los requisitos para este laboratorio son:

* Máquina Wserver 2019 controlador de dominio + DNS + IIS
* Máquina Ubuntu 22.04 CA Root
* Máquina Ubuntu 22.04 CA Subordinada
* Máquina Windows 10 Cliente para hacer pruebas

Partiremos de que tenemos un DC instalado y configurado, con direccionamiento estático, y el rol de IIS activado. El cliente windows 10 unido al dominio, y las máquinas ubuntu actualizadas. Al menos las máquinas ubuntu requieren de acceso a internet para descargar el software de CA (Step-CA).

#### Instalación Step-CA

Previamente la CA debe tener nombre de equipo establecido una IP estática.

```bash
# Actualizar repositorios
apt update

# Instalar curl y wget(si no se tiene)
apt install curl wget -y

# Instalar ultima version Step-CA
wget https://dl.smallstep.com/certificates/docs-ca-install/latest/step-ca_amd64.deb
sudo dpkg -i step-ca_amd64.deb

# Buscar ultima version Step-Cli
wget https://dl.smallstep.com/cli/docs-ca-install/latest/step-cli_amd64.deb
sudo dpkg -i step-cli_amd64.deb

# Crear directorio step-ca y añadir al PATH
sudo mkdir /etc/step-ca
sudo su
export STEPPATH=/etc/step-ca 

```

#### Inicializar CA
```bash
step ca init
```

* Seleccionar **standalone**
* Introducir **nombre** para la **CA**
* Introducir **nombre DNS o ip** de la CA
* Introducir **puerto de escucha de la CA**, ej 443
* Introducir un **mail** para el primier **provisioner**
* Introducir contraseña para la **CA**

#### Añadir ACME provisioner
```bash
# Añadir acme provisioner
step ca provisioner add acme --type ACME

```

#### Cambiar duración certificados 
```bash
# Editar la configuracion de la CA con el siguiente contenido, meteiendolo dentro de cada provisionar, si se quiere cambiar la duración de los certificados, por defecto 24h(OPCIONAL).

sudo nano /etc/step-ca/config/ca.json

```

```
"claims": {  
"maxTLSCertDuration":"26280h",  
"defaultTLSCertDuration":"8760h"  
},
```

#### Lanzar el servicio
```bash
step-ca <fichero_configuracion>

# Ejemplo
step-ca /etc/step-ca/config/ca.json
```

#### Importar certificado de CA Root en clientes
Para que un cliente o servidor pueda confiar en los certificados emitidos por la CA, es IMPRESCINDIBLE que, ya bien de forma automática a través de GPO, o manual instalando el certificado, se instale el certificado de la CA ROOT.

#### Generar certificados auto-renovables
Ya con todo configurado, nos dirigimos al servidor que queremos certificar y descargamos **win-acme**. Al descomprimir editamos las **URL** para que quede de la siguiente manera:
```bash
    "DefaultBaseUri": "https://caroot.midominio/acme/acme/directory",
    "DefaultBaseUriTest": "https://caroot.midominio/acme/acme/directory",
    "DefaultBaseUriImport": "https://caroot.midominio/acme/acme/directory",
```

* Teniendo en cuenta lo configurado en el ca.json. Tanto el ca.json como el DNS deben hacer referencia al mismo nombre: **caroot.midominio**. 

* Abrir el puerto 80 en el firewall del servidor que queremos certificar y lanzar **wacs.exe** como administrador.

* Elegimos la opción de IIS y seguimos los pasos. En caso de querer crear un certificado manual, por ejemplo para el **cliente1.midominio**, cuando nos pregunte el nombre, tenemos que darle justo **cliente1.midominio** ya que hace una validación, y no podemos generar algo que no corresponde a nuestra máquina.