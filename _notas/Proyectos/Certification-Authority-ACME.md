---
title: "Certification Authority + Acme"
layout: single
category: "Proyectos"
slug: "proyectos/certification-authority-acme"
date: 2025-09-30
---

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
* Máquina Windows 10 Cliente para hacer pruebas

Partiremos de que tenemos un DC instalado y configurado, con direccionamiento estático, y el rol de IIS activado. El cliente windows 10 unido al dominio, y la máquina ubuntu actualizadas Al menos la máquina ubuntu requiere de acceso a internet para descargar el software de CA (Step-CA).

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

### Crear certificado de manera manual
Desde la propia CA, donde primero le pasamos el nombre, luego el certificado a exportar y por ultimo la clave que queremos generar.
```bash
step ca certificate web1.et.ms.esp certificado.crt clave.key
```

#### Certificado con tiempo de expiración personalizado
```bash
step ca certificate --not-after="2025-04-11T00:00:00Z" dominio.local certificado.crt clave.key
```

#### Importar certificado de CA Root en clientes
Para que un cliente o servidor pueda confiar en los certificados emitidos por la CA, es IMPRESCINDIBLE que, ya bien de forma automática a través de GPO, o manual instalando el certificado, se instale el certificado de la CA ROOT.

## Crear CASUB en Linux (Pdte probar)
Partiendo que ya tenemos una CA ROOT, nos creamos una maquina llamada CA SUB, y descargamos el software de CA, configuramos direccionamiento y hostname. Posteriormente, teniendo el certificado y la key de la ROOT:
```bash
step ca init --root=[ROOT_CERT_FILE] --key=[ROOT_PRIVATE_KEY_FILE]
```

### Solicitar certificados con Win-Acme
#### Configurar win-acme
Ya con todo configurado, nos dirigimos al servidor que queremos certificar y descargamos **win-acme**. Al descomprimir editamos las **URL** para que quede de la siguiente manera:
```bash
    "DefaultBaseUri": "https://caroot.midominio/acme/acme/directory",
    "DefaultBaseUriTest": "https://caroot.midominio/acme/acme/directory",
    "DefaultBaseUriImport": "https://caroot.midominio/acme/acme/directory",
```

* Teniendo en cuenta lo configurado en el ca.json. Tanto el ca.json como el DNS deben hacer referencia al mismo nombre: **caroot.midominio**. 

* Abrir el puerto 80 en el firewall del servidor que queremos certificar y lanzar **wacs.exe** como administrador.

* Configurar el settings para la "autorenovacion", lo ideal es que sea cada 24h, y en el ca.json se tenga que caduquen los certificados cada 48h. (asi tenemos 24h de margen entre la caducidad y la renovación).


#### Generar certificado autorenovable IIS
* Abrir **win-acme** como administrador, y veremos un menú que iremos contestando preguntas:
```bash
1. Create certificate (full options)
2. Read bindings from IIS
3. Nos pedirá que identificador de sitio elegir, si solo tenemos uno, pulsamos enter.
4. Nos preguntará los bindigs, elegimos "All", luego pulsamos "enter, o 'y' para continuar"
5. Nos pode el "Friendly name", escribimos en nombre, ej: "web1.midominio.com"
6. Nos pregunta si queremos generar certificados por cada dominio, host, etc. Marcamos "Single certificate".
7. En el tipo de verificación se puede dejar la que viene por defecto.
8. Tipo de clave privada "RSA"
9. En lugar de almacenamiento dejamos el por defecto "Windows Certificate Store"
10. En "store to use", dejamos el "default"
11. Por último nos pregunta si queremos sacar una copia del certificado. Aquí marcar lo que interese.
12. Marcamos para crear o actualizar los bindings en IIS
13. Si queremos crear un nuevo binding para otro sitio, es el momento, sino, por defecto es que no.
```

#### Generar certificado web con validación DNS (No auto-renovable)

* Primero debemos abrir **Win-acme** desde el terminal. Para evitar problemas, mejor abrir sin caché:
```bash
cd C:\Win-acme\
wacs.exe --nocache
```
+ Segundo, seguimos el wizzard para generar el certificado:
```bash
* M: Create certificate (full options)
* 2: Manual input
* Aquí metemos el FQDN de la máquina, ej: n111epo1.midominio.local
* Friendly name: podemos dejar por defecto
* Split this source into multiple certificates: por defecto
* Validation: [dbs] Create verification records manually
* Tipo de clave privada: por defecto
* Almacenar el certificado: Va por la necesidad del servicio, elegir lo que corresponda.

```
* Tercero. Al finalizar todo llegaremos a un apartado donde nos pedirá crear una entrada TXT en el DNS. nos vamos al DNS del PDC y creamos una entrada de tipo TXT llamada:
```bash
_acme-challenge.servidor

ejemplo: _acme-challenge.portalweb
```

En su valor, meteremos el que nos pida **win-acme** en el apartado "Content:"

Esta entrada es temporal y le meteremos como valor el challenge que nos dará win-acme más adelante. (Posteriormente win-acme nos pedirá eliminar la entrada).

Terminará creando el certificado y poniéndolo donde le hayamos dicho en pasos anteriores (sea en una ruta, o en el almacén de certificados).

### Generar certificado a partir de un CSR

#### Con step ca (desde la CA)
```
step ca sign request.csr certificado.crt

# Donde request.csr es el CSR generado por el servidor que se quiere certificar, y certificado.crt es el certificado que vamos a generar.
```


#### Certificar Exchange (Autorenovable)

En el DNS deben estar creadas las entradas:
+ mail
+ webmail
+ autodiscover
+ (el nombre de la maquina/host)

Luego con win-acme:
```bash
wacs.exe --source manual --host mail.example.com,webmail.example.com,autodiscover.example.com,host.et.ms.esp --certificatestore My --acl-fullcontrol "network service,administrators" --installation iis,script --installationsiteid 1 --script "./Scripts/ImportExchange.v2.ps1" --scriptparameters "'{CertThumbprint}' 'IIS,SMTP,IMAP' 1 '{CacheFile}' '{CachePassword}' '{CertFriendlyName}'"
```

### Tipo de certificado (segun servidor)
	* JCHAT: WEB tipo PEM
	* EPO: WEB tipo PEM
	* IIS: autorenovable IIS
	* Vcenter: tipo CASUB
	* Exchange: autorenovable con comando "específico"
	* Vcenter: WEB con CSR
	* ESXi: Automatico con Vcenter
