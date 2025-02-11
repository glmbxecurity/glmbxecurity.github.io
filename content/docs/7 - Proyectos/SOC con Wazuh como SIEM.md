# SOC con Wazuh como SIEM

En este proyecto se tratará de montar un SOC en Vmware Workstation, pero toalmente funcional, se irá actualizando poco a poco. Los elementos principales con los que se va a contar son:
* SIEM (Wazuh)
* IDS (Suricata)
* Adversary simulation (Caldera)
* Honeypots
* pFsense (Enrutar, NATear y aislar las distintas redes)
# Índice

1. [SOC con Wazuh como SIEM](#soc-con-wazuh-como-siem)
   1.1. [Elementos principales](#elementos-principales)
   
2. [Planeamiento](#planeamiento)
   2.1. [Redes y conexiones](#redes-y-conexiones)
   2.2. [IMPORTANTE](#importante)

3. [📌 Configuración de Máquinas Virtuales y Redes](#-configuración-de-máquinas-virtuales-y-redes)
   3.1. [Tabla de configuración de redes](#tabla-de-configuración-de-redes)

4. [📌 Tabla de Credenciales del Laboratorio](#-tabla-de-credenciales-del-laboratorio)

5. [Esquema de red](#esquema-de-red)

6. [Requisitos previos](#requisitos-previos)
   6.1. [Configuración en Windows](#configuración-en-windows)
   6.2. [Configuración en Linux (Debian 12)](#configuración-en-linux-debian-12)

7. [Instalación y configuración pFsense](#instalación-y-configuración-pfsense)
   7.1. [Configuración de interfaces en pFsense](#configuración-de-interfaces-en-pfsense)
   7.2. [Reglas de firewall](#reglas-de-firewall)
   7.3. [Configuración firewall WAN Interface](#configuración-firewall-wan-interface)
   7.4. [Configuración firewall SOC Interface](#configuración-firewall-soc-interface)
   7.5. [Configuración firewall HONEYPOT Interface](#configuración-firewall-honeypot-interface)

8. [Instalación y configuración Wazuh](#instalación-y-configuración-wazuh)
   8.1. [Instalación de Wazuh](#instalación-de-wazuh)
   8.2. [Generación de ficheros de configuración e instalación](#generación-de-ficheros-de-configuración-e-instalación)
   8.3. [Deshabilitar repositorios Wazuh](#deshabilitar-repositorios-wazuh)

9. [Instalación y configuración Suricata](#instalación-y-configuración-suricata)
   9.1. [Instalación de Suricata](#instalación-de-suricata)
   9.2. [Configuración de Suricata](#configuración-de-suricata)
   9.3. [Comprobación de alertas](#comprobación-de-alertas)
   9.4. [Envío de logs de Suricata a Wazuh](#envío-de-logs-de-suricata-a-wazuh)

10. [Instalación y configuración Honeypot](#instalación-y-configuración-honeypot)
    10.1. [Instalación de Honeypot](#instalación-de-honeypot)
    10.2. [Lanzar Honeypot](#lanzar-honeypot)
    10.3. [Lanzar honeypots](#lanzar-honeypots)

11. [Instalación e inicio Caldera](#instalación-e-inicio-caldera)
    11.1. [Instalación de Caldera](#instalación-de-caldera)
    11.2. [Alternativa Docker](#alternativa-docker)

12. [File Integrity Monitoring (FIM)](#file-integrity-monitoring-fim)
13. [Custom SCA con Wazuh](#custom-sca-con-wazuh)
14. [CONTINUARÁ EL DESARROLLO CON:](#continuará-el-desarrollo-con)
    14.1. [CDB lists](#cdb-lists)
    14.2. [VirusTotal integration](#virustotal-integration)
    14.3. [Windows defender logs integration](#windows-defender-logs-integration)
    14.4. [Sysmon integration](#sysmon-integration)
    14.5. [TheHive + Cortex](#thehive-cortex)
    14.6. [MISP](#misp)
    14.7. [Shuffle SOAR](#shuffle-soar)
    14.8. [Active response scripts](#active-response-scripts)
    14.9. [Threat Hunting](#threat-hunting)

# Planeamiento
Lo primero que se va a planear son las redes y conexiones, tendremos 3 redes:
* LAN: será la que de acceso a la WAN
* SOC: donde tendremos Wazuh, Suricata y Caldera
* SERVERS: donde tendremos el Honeypot

### IMPORTANTE
Al diseñar el laboratorio en vmware workstation (linux), no funciona el modo promiscuo para suricata, o al menos yo no lo conseguí hacer funcionar, algo imprescindible para el "sniffing" de paquetes de la red de Honeypot.  Para ello se necesitaría o:
* Poner suricata de proxy entre honeypot y pfsense
* Un switch físico y hacer port-mirroring hacia un interfaz de suricata
* Realizar el laboratorio en workstation Windows (teóricamente funciona)

No obstante, se ha detallado el proyecto para que puedas realizarlo de una de estas 3 maneras. En mi caso, la máquina suricata llevará el honeypot integrado, es decir, Suricata + Honeypot en la misma MV.

La guía se puede seguir perfectamente, a la hora de instalar el honeypot, se avisará de lo que hay que hacer (caso de usar Vmware Workstation en Linux)
## **📌 Configuración de Máquinas Virtuales y Redes **

| **Máquina Virtual** | **Interfaz**      | **IP**            | **VMnet**            | **Función**                     |
| ------------------- | ----------------- | ----------------- | -------------------- | ------------------------------- |
| **pfSense**         | `WAN (le0)`       | **192.168.1.200** | `VMnet0 (Bridge)`    | Conexión a Internet             |
|                     | `LAN1 (le1)`      | **10.0.1.200/24** | `VMnet1 (Host-Only)` | Red SOC (Administración pf)     |
|                     | `LAN2 (le2)`      | **20.0.1.200/24** | `VMnet2 (Host-Only)` | Red Honeypot                    |
| **Suricata**        | `ens33` (Gestión) | **20.0.1.2/24**   | `VMnet2 (Host-Only)` | Red Honeypot (IDS)              |
| **Wazuh + Caldera** | `ens33`           | **10.0.1.2/24**   | `VMnet1 (Host-Only)` | Red SOC                         |
| **Kali Linux**      | eth0              | **10.0.1.1/24**   | `VMnet1 (Host-Only)` | Red SOC (Atacante pruebas)      |
| **Honeypot**        | `ens34`           | **20.0.1.1/24**   | `VMnet2 (Host-Only)` | Red Honeypot (Atacada)          |


---

## **📌 Tabla de Credenciales del Laboratorio**

| **Máquina/Servicio**                 | **Usuario**     | **Contraseña**                     | **Notas**                                                               |
| ------------------------------------ | --------------- | ---------------------------------- | ----------------------------------------------------------------------- |
| **pfSense Web GUI**                  | `admin`         | `cuTRfyC6OOCui6`                   | Acceso a la interfaz web solo en la **Red SOC** (`https://10.0.1.200`)  |
| **pfSense SSH**                      | `admin`         | `cuTRfyC6OOCui6`                   | Acceso remoto por SSH solo desde la **Red SOC** (`ssh root@10.0.1.200`) |
| **Honeypot (Cowrie, Dionaea, etc.)** | `root`          | `honeypot123`                      | Dependiendo del honeypot instalado                                      |
| **Wazuh Web UI**                     | `admin`         | `kpAGnmrQHiymIWRnO?mPEh*L46NJo6.e` | Acceso a la consola Wazuh (`https://10.0.1.1`)                          |
| **Wazuh SSH**                        | `administrator` | `SOCproyecto.2025!`                | Acceso al servidor Wazuh                                                |
| **Suricata SSH**                     | `administrator` | `SOCproyecto.2025!`                | Acceso al servidor Suricata (`10.0.1.2`)                                |
| **Caldera (Red Team Framework)**     | `admin`         | `SOCproyecto.2025!`                | Acceso a `https://10.0.1.1:8888`                                        |
| **Kali linux**                       | `kali`          | `kali`                             |                                                                         |


### Esquema de red
![Esquema_Red](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/SOC/esquema%20l2_l3.png)

## Requisitos previos
Para no extender mucho esta guía, se omitirán ciertos pasos pero que son requisito previo e indispensable:
* Crear Vmnets
* Asegurarse que el Vmnet0 en modo bridge está en bridge con la interfaz deseada
* Configurar router de la red de casa para:
	* pFsense (192.168.1.200) tenga todos sus puertos abiertos. Se puede meter en DMZ
	* Reenvío de tráfico de los servicios que queramos ser atacados hacia el pFsense

* Configurar el equipo anfitrión en la red de SOC para poder acceder a las interfaces de wazuh, caldera, etc.

	#Windows
	Tan sencillo como editar la interfaz desde el administrador de interfaces
	
	#Linux (Debian 12)
	Crear un fichero para el interfaz:
	sudo nano /etc/systemd/network/10-vmnet1.network (Para otras ocasiones solo cambiar el vmnet, lo del "10-" se mantiene).
	```bash
	[Match]
	Name=vmnet1
	
	[Network]
	Address=10.0.1.3/24
	Gateway=10.0.1.200
	```
	
`sudo systemctl restart systemd-networkd`


## Instalación y configuración pFsense

Una vez tengamos la MV instalada, le agregaremos 3 interfaces de red conectados a: 
* Vmnet0 será la WAN
* Vmnet1 será SOC
* Vmnet2 será Honeypot

Se habilita el interfaz, asignamos un nombre, establecemos IP estática, cambiamos el CIDR y nos aseguramos que la interfaz de WAN, su gateway de "upstream" sea la gw de tu red local de casa.
![pfsense_interfaces](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/SOC/pfsense_interfaces.png)

El siguiente paso es configurar las reglas de firewall, las principal intención de comunicación es:
* Honeypot puede ser accedido dese WAN (para ser atacado)
* Honeypot puede acceder a SOC (para enviar logs a Wazuh)
* Honeypot puede ser accedido desde SOC (Para acceder desde Kali, Wazuh, Caldera, etc)
* Suricata NO puede ser accedido desde WAN (no tiene motivos para ello)
* Suricata puede acceder a WAN (buscar updates)
* Suricata puede acceder a SOC (enviar logs a Wazuh)
* Suricata puede ser accedido desde SOC
* SOC puede acceder a WAN (updates e internet)
* SOC NO puede ser accedido desde WAN (no tiene motivos para ello)

![firewall_map](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/SOC/firewall_map.png)

### Configuración firewall WAN Interface
![firewall_map](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/SOC/firewall_wan.png)
  
### Configuración firewall SOC Interface
![firewall_map](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/SOC/firewall_so.png)
  
### Configuración firewall HONEYPOT Interface
![firewall_map](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/SOC/firewall_honeypot.png)
## Instalación y configuración Wazuh

Instalamos (En mi caso Ubuntu Server 22.04), asignamos Vmnet1, establecemos direccionamiento IP (10.0.1.2/24 - Gw 10.0.1.200).

```bash
apt update && apt upgrade -y
```

___NOTA:Dependiendo de la versión de wazuh, los comandos pueden variar, lo mejor es consultar la documentación oficial___


15. Descargar el script de instalación (la URL variará)
```bash
curl -sO https://packages.wazuh.com/4.10/wazuh-install.sh
curl -sO https://packages.wazuh.com/4.10/config.yml
```

16. Editar el config.yml con el hostname de la MV y la IP
![firewall_map](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/SOC/wazuh-indexer-install.png)

17. Generar ficheros de configuración e instalar
```bash
bash wazuh-install.sh --generate-config-files
bash wazuh-install.sh -a
```

18. Eliminar repositorios de wazuh, para evitar un upgrade accidental que pueda estropear el servicio. (OPCIONAL)
```bash
sed -i "s/^deb /#deb /" /etc/apt/sources.list.d/wazuh.list
apt update
```

## Instalación y configuración Suricata

Instalamos el S.O, asignamos 2 interfaces de red al Vmnet1, y establecemos direccionamiento IP.

```bash
apt update && apt upgrade -y
add-apt-repository ppa:oisf/suricata-stable
apt install suricata -y



# Descargar emmerging rules
cd /tmp/ && curl -LO https://rules.emergingthreats.net/open/suricata-6.0.8/emerging.rules.tar.gz  
sudo tar -xvzf emerging.rules.tar.gz && mkdir /etc/suricata/rules && sudo mv rules/*.rules /etc/suricata/rules/  
	sudo chmod 640 /etc/suricata/rules/*.rules


```

19. Editar configuración para especificar la interfaz de red, y la HOME_NET (la red que queremos monitorear), ademas de las nuevas rules descargadas.

```bash
/etc/suricata/suricata.yml

# buscar esta linea y editar tal que así
af-packet:
  - interface: ens33

#buscar la esta linea y editar con las redes que queremos monitorear, en este caso la del soc y la de honeypot
vars:
  # more specific is better for alert accuracy and performance
  address-groups:
    HOME_NET: "[20.0.1.0/24]"

# buscar default-rule y editar tal que asi
default-rule-path: /etc/suricata/rules  
rule-files:  
- "*.rules"
```

20. Habilitar al inicio e iniciar
```bash
systemctl enable suricata
systemctl start suricata
```

21. Comprobar alertas
```bash
#Ya deberiamos ver los scans de nmap, por ejemplo
tail -f /var/log/suricata/fast.log
```

### Envío logs Suricata > Wazuh
Para ello necesitaremos tener un agente de Wazuh instalado en suricata. En el panel de Wazuh > Deploy Agents. Rellenamos con la IP del servidor, elegimos S.O destino, etc. y nos generará un comando similar al siguiente, que descargará el agente de los servidores de Wazuh (internet) con la configuración deseada. En caso de ser offilne, se puede descargar e importar el agente de manera offline.
```bash
wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.10.1-1_amd64.deb && sudo WAZUH_MANAGER='10.0.1.2' dpkg -i ./wazuh-agent_4.10.1-1_amd64.deb
```


Editamos el siguiente fichero para decirle al agente de wazuh donde están los logs:
___Si no funciona, agregar tambien al fichero ossec.conf del manager, desde la interfaz web___
```bash
/var/ossec/etc/ossec.conf


# eal final del fichero en el ultimo <ossec_config> (no en el primero)
	
	<localfile>
		<log_format>syslog</log_format>
		<location>/var/log/suricata/eve.json</location>
	</localfile>
```

Por último habilitamos el servicio y lo iniciamos:
```bash
sudo systemctl daemon-reload 
sudo systemctl enable wazuh-agent 
sudo systemctl start wazuh-agent
```

### Instalación y configuración Honeypot

Llegados a este punto, si virtualizas en workstation con linux, debes agregar una regla para permitir el tráfico desde WAN hacia suricata. Si tu caso es cualquier otro descrito en esta guía, puedes seguir normalmnete., teniendo en cuenta en que MV instalar el Honeypot.

#### Instalación
```bash
apt
apt install python3-pip
pip install honeypots
```

### Lanzar honeypot
Honeypots tiene una larga lista de servicios que se pueden lanzar, para ver el listado:

##### Listar honeypots
```bash
honeypots --list
```


##### Lanzar honeypot
```bash

# Ejepmplo lanazr SSH
python3 -m honeypots --setup ssh --auto

# Lanzar todos:
python3 -m honeypots --setup all --auto
```


### Instalación e inicio Caldera
Caldera es un servicio para la emulación del adversario, de esta manera podremos lanzar ataques simulados a nuestro honeypot y comprobar la detección por parte de wazuh.

```bash
git clone https://github.com/mitre/caldera.git --recursive
cd caldera
pip3 install -r requirements.txt

#### INICIAR EL SERVICIO
python3 server.py --insecure --build
```

#### Instalación docker (alternativa)
```bash
# Recursively clone the Caldera repository if you have not done so
git clone https://github.com/mitre/caldera.git --recursive

# Build the docker image. Change image tagging as desired.
# WIN_BUILD is set to true to allow Caldera installation to compile windows-based agents.
# Alternatively, you can use the docker compose YML file via "docker-compose build"
cd caldera
docker build . --build-arg WIN_BUILD=true -t caldera:latest

# Run the image. Change port forwarding configuration as desired.
docker run -p 8888:8888 caldera:latest
```

Tras el despliegue, debemos desplegar un agente en el honeypot, para lanzar los ataques simulados y ver si en wazuh vemos los detalles de esos ataques. 

##### ACCESO
`https://<ip>:8888`

### File Integrity Monitoring (FIM)
Trata de monitorizar la integridad de ciertos ficheros y directorios importantes. para ello en el agente de la MV en cuestión (honeypot), debemos agregar los directorios y/o ficheros que queramos monitorizar.

Dependiendo de la maquina, en un entorno real, unos directorios serán importantes y otros no. Debemos conocer nuestro servicio y la criticidad para saber determinar que es importante y que no.

```bash
## EQUIPO CLIENTE LINUX CON AGENTE WSUS
/var/ossec/etc/ossec.conf

# Apartado de File integrity monitoring
<syscheck>
  <disabled>no</disabled>
  <frequency>720</frequency>
  <scan_on_start>yes</scan_on_start>
  <directories check_all="yes" report_changes="yes" real_time="yes">/etc,/bin,/sbin</directories>
  <directories check_all="yes" report_changes="yes" real_time="yes">/lib,/lib64,/usr/lib,/usr/lib64</directories>
  <directories check_all="yes" report_changes="yes" real_time="yes">/var/www,/var/log,/var/named</directories>
  <ignore>/etc/mtab</ignore>
  <ignore>/etc/hosts.deny</ignore>
  <ignore>/etc/mail/statistics</ignore>
  <ignore>/etc/random-seed</ignore>
  <ignore>/etc/adjtime</ignore>
  <ignore>/etc/httpd/logs</ignore>
  <ignore>/etc/utmpx</ignore>
  <ignore>/etc/wtmpx</ignore>
  <ignore>/etc/cups/certs</ignore>
  <ignore>/etc/dumpdates</ignore>
  <ignore>/etc/svc/volatile</ignore>
  <ignore>/sys/kernel/security</ignore>
  <ignore>/sys/kernel/debug</ignore>
  <ignore>/sys</ignore>
  <ignore>/dev</ignore>
  <ignore>/tmp</ignore>
  <ignore>/proc</ignore>
  <ignore>/var/run</ignore>
  <ignore>/var/lock</ignore>
  <ignore>/var/run/utmp</ignore>
</syscheck>
```

# Custom SCA con Wazuh

El **Security Configuration Assessment (SCA)** es una herramienta clave para evaluar el cumplimiento de estándares de seguridad como **CIS** o **NIST**, verificando configuraciones como el tiempo de desconexión tras inactividad.

Debido a lo extenso que es este apartado, se ha desarrollado en otro artículo, publicado en la siguiente url: [Custom SCA con Wazuh](https://glmbxecurity.github.io/docs/7-proyectos/custom-sca-con-wazuh/)

# CONTINUARÁ EL DESARROLLO CON:
* CDB lists
* VirusTotal integration
* Windows defender logs integration
* Sysmon integration
* TheHive + Cortex
* MISP
* Shuffle SOAR
* Active response scripts
* Threat Hunting



