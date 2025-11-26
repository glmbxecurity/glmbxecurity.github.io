---
title: "Preparacion Ejpt V2"
layout: "single"
category: "Setup"
slug: "setup/preparacion-ejpt-v2"
date: "2025-09-30"
---

![Certificado](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/main/images/ejptcert.jpeg)  

[Link al certificado](https://certs.ine.com/c33d08cb-5b6a-4ce5-af2a-0e5bc5bfdba5#gs.cm2wft)     

### Introducción
En este post se detallará todo lo necesario para afrontar esta certificación con éxito, tanto las técnicas necesarias, máquinas para practiar, metodología de examen, contenidos, etc.  

### Indice
* [Que es eJPTv2]()  
* [El examen]()  
* [Conocimientos necesarios]()  
* [Metodología]()  
* [Donde prepararse]()  
* [Máquinas CTF]()  
* [Diccionarios utilizados]()

### Que es eJPTv2
eLearning Junior Penetration Tester, es una certificación en ciberseguridad 100% práctica ideal para aquellos que se quieran iniciar en la ciberseguridad. Es de las mas asequibles en este campo, pero no por ello es trivial, requiere de esfuerzo, dedicación y mucha práctica.



### El examen
El examen consiste en vulnerar entre 3-5 máquinas virtuales aproximadamente, tanto Linux como Windows y contestar unas preguntas que se plantean para comprobar que se ha llevado a cabo la intrusión correctamente, como por ejemplo cantidad de usuarios en una máquina X, o puertos abiertos en máquina Y.

El voucher tiene un precio aproximadamente de 200€/$, e incluye un curso de formación para superar con éxito el examen, además de 2 intentos para aprobar.

### Conocimientos necesarios
Antes de iniciar el curso (cosa que no es obligatoria), se deben tener conocimientos básicos a nivel de redes, incluido routing, conocimientos básicos de Windows, Linux, CMD, bash, scripting, html y css, además es recomendable conocer lo básico a nivel programación (si es python mejor).

Además de esto básico, se requiere conocer las siguientes técnicas:
* Descubrimiento de equipos y subdominios
* Uso de Nmap
* Codificación / decodificación (Ej: Base64)
* Crackeo de ficheros comprimidos
* Uso de Metasploit y Msfvenom
* Establecimiento de reverse shells
* Capacidad de análisis de capturas en Wireshark
* Fuzzing Web
* Descubrimiento y hacking CMS
* Local file inclusion
* File upload y bypass de extensiones
* Fuerza bruta contra paneles de login web
* Fuerza bruta contra FTP, SSH
* Uso de monturas
* Enumeración y hacking SMB (SMBmap), SNMP, TOMCAT
* SQL injection con SQLmap
* Escalada de privilegios Linux (SUID, Sudo -L, capabilities, tareas cron...)
* PATH Hijacking
* Pivoting de usuarios
* Tratamiento de TTY (Linux)
* Búsqueda y explotación de vulnerabilidades Windows (sencillas)
* Escalada de privilegios Windows (con Metasploit, sencillas)
* Pivoting con Metasploit

### Metodología de examen
A la hora de enfocar el examen es muy importante ser ordenado, metódico y apuntar absolutamente todo lo que veamos medianamente importante con herramientas como "Cherry Tree" u "Obsidian", ya que nos ahorrará mucho tiempo más adelante. 

Es muy importante enumerar, enumerar y enumerar, todo lo que se pueda. Nunca se sabe por donde puede venir la intrusión.

Probar todas las técnicas conocidas, y aprovechar de la herramienta Metasploit ya que no tendremos acceso a internet para descargar exploits de ningún sitio. Los laboratorios de examen están diseñados para ser vulnerados con el kali que nos dan, sin necesidad de acceder a internet.

Toma tus propios apuntes y crea tu Cheatsheet, ya que te ayudará en el examen y no perderás tiempo buscando por internet como se hace esto o lo otro.

### Dónde prepararse
En principio con la formación que incluye el voucher es más que suficiente para apbrobar, pero si es cierto que se antoja muy extensa. Mi recomendación es que tomes el curso de **Preparación para la eJPTv2** de **Formula Hacking**, o el curso de **Introducción al hacking** de **Hack4u** . Aunque este último comienza desde 0 y asienta unas buenas bases, luego se complica muchísimo más que la eJPTv2 y quizás su contenido puede parecer abrumador. Mi consejo es combinar ambos para ver las técnicas descritas en el apartado anterior.
### Máquinas CTF para practicar
Después de ver los cursos y aprender, toca practicar lo aprendido, aquí te dejo un listado de máquinas vulnerables para practicar el examen que te servirán de apoyo y refuerzo de lo aprendido.

#### Vulnhub

* Dark Hole 1✔️- [Writeup](https://www.linkedin.com/posts/edward-herrera-galamba-77a92513b_writeup-ctf-darkhole-vulnhub-activity-7162120686814150656-6t9a?utm_source=share&utm_medium=member_desktop)
* Symfonos 1 ✔️- [Writeup](https://www.linkedin.com/posts/edward-herrera-galamba-77a92513b_symfonos-1-vulnhub-activity-7163626204149886976-P2AI?utm_source=share&utm_medium=member_desktop)
* Dark Hole 2 ✔️ - [Writeup](https://www.linkedin.com/posts/edward-herrera-galamba-77a92513b_darkhole-lab-activity-7186023841960189952-aE-X?utm_source=share&utm_medium=member_desktop)
* Symfonos 2 ✔️
* Symfonos 3 ✔️
* Symfonos 5 ✔️ - [Writeup](https://glmbxecurity.github.io/docs/10-writeups/symfonos-5/)
* Election ✔️
* Hack me please 1 
* Insanity
* ICA 1
* Corrosion 2
* Venom 1
* Durian 1

#### HackTheBox
Linux
  - Antique Linux 
  - Armageddon 
  - Blocky Linux
  - Bolt Linux PassBolt
  - GoodGames 
  - Hawk Linux 
  - Horizontall Linux
  - Lame Linux Samba
  - Nibbles Linux
  - Oopsie Linux
  - Shocker Linux
  - Tabby Linux LFI
  - Union Linux SQL
  - Validation Linux
Windows
  - Archetype 
  - Devel Windows 
  - Driver Windows
  - Grandpa Windows
  - Granny Windows
  - Jeeves Windows
  - Jerry Windows
  - Legacy Windows
  - Love Windows
  - Netmon Windows
  - Return Windows



#### Tryhackme
* Blue✔️
* Ice ✔️
* Blaster ✔️
* Pentesting Fundamentals ✔️
* Ignite ✔️
* Blog ✔️
* Startup✔️
* Chill Hack ✔️
* VulnNet: Internal✔️
* ColdBox: Easy✔️
* Basic pentesting
* Vulnversity ✔️
* takeover
* Rootme✔️
* Pickle rick✔️
* SkyNet
* Chocolate factory
* Easy peasy
* Corridor
* Steel Mountain
* Game Zone

#### PG play
* Dawn
* InfosecPrep
* Seppuku
* FunBoxEasy

#### HackMyVM
* Friendly
* Art

### Diccionarios utilizados eJPTv2
##### Fuerza bruta login FTP y SSH
* __/usr/share/metasploit-framework/data/wordlists/common_users.txt__
* __/usr/share/metasploit-framework/data/wordlists/common_passwords.txt__

##### Fuerza bruta SAMBA passwords
* __/usr/share/metasploit-framework/data/wordlists/unix_users.txt__
* __/usr/share/metasploit-framework/data/wordlists/unix_passwords.txt__

#### Fuzzing web
* __/usr/share/metasploit-framework/data/wmap/wmap_dirs.txt_

#### HTTP Login
Passwords
* __/usr/share/metasploit-framework/data/wordlists/http_default_pass.txt_ 
* Users
* __/usr/share/metasploit-framework/data/wordlists/http_default_users.txt_
* * __/usr/share/metasploit-framework/data/wordlists/namelisttxt_

Users:Passwords (usuario y contraseña separado por ":")
* __/usr/share/metasploit-framework/data/wordlists/http_default_userpass.txt__
