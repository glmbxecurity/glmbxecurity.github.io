---
title: "DNS & mail reccon"
layout: "single"
category: "Reconocimiento"
slug: "reconocimiento/dominios-y-emails"
date: "2025-09-30"
---

### Reconocimientos pasivos
Con phonebook.cz se pueden reconocer subdominios de empresas expuestas, pero también podemos usar una herramienta por consola, llamada **CTFR**  
  
* [CRT.SH](https://crt.sh/)
* [Phonebook.cz](https://phonebook.cz)
* [Dnsdumpster](https://dnsdumpster.com) (muy buena para reconocimiento de un dominio)

#### Sublist3r
```bash
./sublist3r.py -d acmeitsupport.thm
```
#### DNSrecon
```bash
dnsrecon -t brt -d acmeitsupport.thm
```

#### Claves filtradas
Si encontramos un email de una organización, podemos ir a haveibeenpwned.com para ver si ese email tiene claves filtradas.

#### theHarvester
Herrramienta para descubrir emails, nombres, subdominios, urls... Con la opcion -b le decimos que motores de búsqueda utiliza, para ver una lista completa ir a su [Repositorio de github](https://github.com/laramies/theHarvester)
```bash
theHarvester -d miweb.com -b google,linkedin,yahoo,dnsdumpster,duckduckgo,crtsh
```
### Reconocimientos activos

#### Dnsenum
```bash
dnsenum midominio.com
```

#### Dig
```bash
dig axfr @servidorDNS dominio.local
```

#### Fierce
```bash
fierce -dns dominio.com 

# Especificando un diccionario
fierce -dns dominio.com -wordlist <diccionario para fuzzing dns>
```

#### GObuster
 Con esta herramienta se pueden realizar varios tipos de fuzzing, entre ellos el de subdominios. se podría filtrar los errores que no queremos que aparezcan con un grep -v (para excluir lineas)
 ```bash
 gobuster vhost -u <url> -w <diccionario> -t 20 | grep -v "403"
 ```
#### Wfuzz
 Igual que gobuster, aunque un poco mas complicada de usar, tiene mejores filtros y se ve con mas claridad. El modo de uso es parecido para los distintos tipos de fuzzing.
 
 Con la palabra interna reservada ** FUZZ ** la colocamos en la parte que queramos fuzzear, en este caso la que va delante del dominio principal. ahí será donde se prueben los dominios. con "--hc" hide code, excluiriamos el codigo de estado que no nos interese, en este caso el 403
 ```bash
 wfuzz -c -t 20 --hc=404 -w <diccionario> -H "Host: FUZZ.google.com" http://google.com
 ```

