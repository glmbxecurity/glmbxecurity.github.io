
### Whatweb 
 ```bash
 whatweb xiaomi.com
 ```

### Gobuster
Con gobuster tenemos la opción para especificar que estamos ante virtual hosting, y extensiones de archivos.
 ```bash
 gobuster dir -u http://xiaomi.com/ -t 50 -w <dicionario>
  gobuster dir -u http://xiaomi.com/ -t 50 -w <dicionario> -x php,html,txt,py,sh,js
 gobuster vhost  -u driftingblues.box -w /usr/share/wordlists/dirb/common.txt
 ```

### Dirb
Dirb hace automáticamente fuzzing sobre los directorios encontrados para localizar subdirectorios.
```bash
dirb <http://ip>
dirb <http://ip> /ruta/diccionario/personalizado
```
#### Fuzzing web HTTPS
Nos saldrá un error al usar SSL, y nos dirá los codigos que debemos omitir para no tener errores, como ejemplo se puso el codigo de estado 200
```bash
#OPCION 1
gobuster dir -u 'https://ip' -w <diccionario> -k
#OPCION 2
gobuster dir -u 'https://ip' -w <diccionario> -k -l -s '200'
```
### Wfuzz
 ```bash
 wfuzz -w <diccionario> -u http://xiaomi.com/FUZZ --hc=403,404
  wfuzz -w <diccionario> -u http://xiaomi.com/FUZZ -x php, html, txt
 wfuzz -t 200 -z range.1-20000 -u 'https://mi.com/shop/buy/detail?product_id=FUZZ'
 wfuzz -t 200 --hw=6515 -z range,1-20000 -u 'https://mi.com/shop/buy/detail?product_id=FUZZ'
 
 ```
### Fuff 
La herramienta FUFF, que es muy potente y además super rápida, además si el codigo de estado es 301, dice a donde redirecciona, por ejemplo:
 ```bash
fuff -t 200 -w <diccionario> -u https://xiaomi.com/FUZZ -v
fuff -t 200 -w <diccionario> -u https://xiaomi.com/FUZZ --mc 200 -v
 con esto le decimos que el codigo de estado sea 200 y en modo verbose
 ```
### Dirsearch
 Tiene su propio diccionario y basta con ejecutar el siguiente comando:  
 
 ```bash
dirsearch -u <URL>
 ```
 * HTTPS: mirar certificado SSL (a veces hay cositas en Common Name)

### Dirb
```bash
dirb http://ip/

dirb http://ip/ /diccionario_directory_list2-3-medium.txt
```

### Metasploit
```bash
use auxiliary/scanner/http/brute_dirs
use auxiliary/scanner/http/robots.txt
```