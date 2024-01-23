En esta página se llevarán a cabo las distintas técnicas que se pueden utilizar para sacarle partido a wireshark en el entorno de la ciberseguridad.

### Encontrar capturas de wireshark
```bash
find / -name *.pcap* 2>/dev/null
```
### Contraseñas con wireshark
Puede darse el caso de que se haya establecido una conexión, una shell, reverse shell, hacia la máquina, y se podría mirar el historial de comandos. Caso muy útil porque podriamos descubirir **contraseñas, o ficheros interesantes**.

#### Forma 1 (Analizando paquetes) (Contraseñas web, sql)
Conociendo la IP y el puerto, por ejemplo web. Si la conexión es por HTTP, la información viaja en texto plano, con lo que podriamos intentar descubrir "logins", que se hayan realizado.

#### Forma 2 (Con strings)(Credenciales de sistema)
Si se ha establecido una terminal remota, (por ejemplo telnet o netcat), la información viaja también en claro. Con lo que se puede hacer un **follow redirection** y wireshark nos muestra los comandos introducidos. o con **strings** y veremos directamente las cadenas de texto legibles sobre el terminal.
```bash
strings captura.pcap
```