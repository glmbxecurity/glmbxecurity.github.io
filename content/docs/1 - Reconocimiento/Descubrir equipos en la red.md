 ```bash
 arp-scan -I <interfaz> --localnet --ignoredups

nmap -sn <dir_red/mask>

 
masscan -p80,8000-8100 10.0.0.0/8 --rate=10000

netdiscover -P -i eth0
netdiscover -P -i eth0 -r 192.168.1.0/24 (debemos poner la dirección de red de la interfaz que queremos escanear)
 ```

Tener en cuenta que **puede haber subnetting**, y esto no impide encontrar equipos en distintas redes.
En caso de haber segmentación de red, no se verian equipos de otra red. Por ejemplo, si tuvieramos la red 10.10.10.0/24 e hicieramos el scan de la siguiente manera: 
```bash
nmap -sn 10.10.0.0/16
```
en caso de haber un equipo, ej: 10.10.54.25/16, y estuviera activo, lo veríamos.

**Las maquinas virtuales comienzan con la mac 08:00:... y tener un branding de PCS Systemtechnik**

### MAC's típicas de Máquina Virtual
* 08:00:XX:XX:XX:XX
* 00:0c:29:XX:XX:XX
#### Brandings de MV
* PCS Systemtechnik
* Vmware

