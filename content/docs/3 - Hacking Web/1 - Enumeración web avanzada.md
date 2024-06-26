### Enumeración con metasploit
Buscar módulos para enumeración http
```bash
search tpye: auxiliary name:http
```

### Enumeracion con WMAP (Metasploit)
```bash
### Cargar modulo wmap
load wmap

### Ver las opciones que tiene
wmap_ (y tabulamos)

### Agregar un sitio
wmap_sites -a <IP>
wmap_sites -l # Listar los sites

### especificar un target
wmap_targets -t <URL>
wmap_targets -l #Listar targets

### Lanzar escaneo por defecto con los modulos habilitados
wmap_run -e
```
### Escaneo vulnerabilidades HTTP
```bash
nmap <ip> -p <puerto> -n -Pn --script=http-enum
```

### Escaneo vulnerabilidades con Nikto
```bash
nikto -url <url>
```
### Buscar comentarios
```bash
curl http://172.16.226.6/ | grep "!"
```

### Ver codigo fuente con CURL
En ocasiones encontramos codigo php que no podemos ver, pero si se interpreta por el servidor. Si queremos conocer su código:
```bash
curl -s "http://ip/fichero.php"
```

### Enumeración cabeceras

Introduciendo cabeceras válidas e inválidas veremos diferentes respuestas. Podemos enumerar si tiene virtual hosting y ver cual es el dominio

```bash
curl -H 'Host: 172.16.226.6' "http://172.16.226.6/'"
```
"<address>Apache/2.4.18 (Ubuntu) Server at 172.16.226.6 Port 80</address>"

```bash

curl -H 'Host: http://172.16.226.6' "http://172.16.226.6/'"
```
<address>Apache/2.4.18 (Ubuntu) Server at driftingblues.box Port 80</address>

### Enumerar subdominios
```bash
nikto -h http://test.driftingblues.box/
```

### Enumerar emails en la web
Con un script de nmap llamado **http-email-harvest** 
```bash
wget https://raw.githubusercontent.com/tixxdz/nmap/master/scripts/http-email-harvest.nse
nmap --script-updatedb
nmap -p80 --script http-email-harvest driftingblues.box

```

### Ver web sin interfaz grafica
```bash
browsh <url>
lynx <url>
```
