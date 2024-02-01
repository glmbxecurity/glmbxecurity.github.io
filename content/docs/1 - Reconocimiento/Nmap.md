
```bash 
nmap <ip> <parametros>
``` 

### Escaneo básico Nmap 

```bash
# Primer escaneo simple para conocer puertos abiertos
nmap 10.10.10.4 -p- --open -n -Pn --min-rate 2000 -oG fichero.txt
nmap 10.10.10.4 --top-ports 10000 --open -n -Pn --min-rate 2000 -oG fichero.txt

# Escaneo a puertos UDP (en ocasiones hay servicios corriendo en un puerto UDP)
nmap 10.10.10.4 -sU --top-ports 200 --min-rate 2000 -Pn -oG fichero.txt

# Escaneo conociendo los puertos abiertos
nmap 10.10.10.4 -p 22,80,445 -n -Pn --min-rate 2000 -sS -sCV -oG fichero.txt
```

### Scripts Nmap
```bash
# Con la opción -sC utiliza el script por defecto para encontrar vulnerabilidades, si queremos utilizar un script específico, podemos consultar el listado de scripts

ls /usr/share/nmap/scripts

# Elegir el script deseado y realizar el escaneo de la siguiente manera
nmap 10.10.10.4 --script "vuln" -p 445
``` 


### Evasion de Firewall con Nmap
Se puede intentar evitar el bloqueo por parte del firewall al intento de escaneo de puertos. para ello algo muy común es el hecho de fragmentar los paquetes, o indicar el tamaño maáximo de MTU (tamaño máximo de transimision de unidad), o falsear ciertos datos.  

* -f (fragmentar paquetes)
* --mtu <numero multiplo de 8>
* -D <ip> (falsificar ip de origen)
* --source port <puerto> (falsificar puerto de origen)
* --data-length <numero> (modificar tamaño de paquete, sumando ese numero al tamaño original del paquete)
* --spoof-mac <mac> (falsear la mac)  
   
 El falseo de IP y MAC, puede ser útil si se combina con el siguiente comando, que nos enumera los dispositivos con su IP y MAC que están conectados y activos en la red:  
 
 arp-scan -I <interfaz> --localnet
 
   
 * -sS (tratar de no dejar evidencias en Firewall/IDS), explicación:  
>Al realizar un escaneo, el atacante envía un SYN, recibe un SYN/ACK, y vuelve a responder con un ACK. Aquí terminaría la conexión. En caso de estar el puerto cerrado o la conexion ser rechazada, recibiriamos un RST en lugar del SYN/ACK.  
Pues bien, con "-sS", lo que hacemos es después de recibir el SYN/ACK, enviamos un RST. Ya que algunos Firewall, solo registran conexiones completas, y al no enviar el ACK, no lo registran en sus logs.

### Parámetros mas frecuentes de nmap
Los parámetros mas útiles son los siguientes:  
* -p1-100 (puertos del 1 al 100)
* -p- (todos los puertos)
* --top-ports 100 (Los 100 puertos mas comunes [en este ejemplo])
* -n (para evitar resolucion DNS)
* -T (del 0 al 5. Indica la velocidad, y por consiguiente la agresividad del escaneo)(un numero mayor puede ser detectado por firewalls)
* -sU (puertos UDP)
* -sV (version del servicio)
* -sn (detectar equipos en la red, mac, y marca)  
* --min-rate 5000 (agiliza bastante el escaneo, no se recomienda añadir mas de 5000)
*  --open (evita puertos filtered)
* -sC (conjunto de scripts de nmap para detectar vulnerabilidades)
*  -Pn (Evitar ping y tratar equipo como activo y alcanzable en la red)
*  -oN (exportar escaneo en formato nmap a un fichero)