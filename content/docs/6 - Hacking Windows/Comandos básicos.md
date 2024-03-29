### Indice
- [Recolectar informacion](#recolectar)
- [Usuarios](#usuarios_grupos)
- [Operaciones con ficheros](#ficheros)
- [Networking](#net)
- [Compartir ficheros entre maquinas](#comp)

### Cheatsheet completa comandos básicos Windows 
[Windows Cheatsheet AIO](https://stationx.net/windows-command-line-cheat-sheet/)
### Recolectar información
```powershell
systeminfo
```
### Usuarios
```powershell
# Mostrar info del usuario
net user <usuario>

# Establecer/cambiar contraseña
net user <usuario> <contraseña>

# Crear usuario
net user <usuario> <contraseña> /add

```

### Operaciones con ficheros

```powershell

dir /A:H (ver ocultos)
cd
mkdir
rmdir
copy
xcopy /s (copiar directorio y subdirectorios)
del
move
ren

C: (Cambiar a disco C)
attrib <fichero> (ver los atributos)


```
### Networking
```powershell
ipconfig /all
nslookup <IP o nombre>

#Ver puertos a la escucha y conexiones abiertas
netstat-an

#Ver recursos compartidos
net view <IP o nombre equipo o localhost>

arp -a

```

### Compartir ficheros entre máquinas
En Windows una opción como curl es **certutil.exe** 
```bash
certutil.exe -f -urlcache http://IP/fichero fichero
```
