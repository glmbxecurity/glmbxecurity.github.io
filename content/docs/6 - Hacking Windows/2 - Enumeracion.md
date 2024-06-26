
### Enumerar usuarios Active Directory
#### Kerbrute - kerberos
Kerbrute es una herramienta que realiza ataques de fuerza bruta contra kerberos para enumerar:
* Parejas de usuario/contraseña válidas
* Usuarios válidos
* Usuarios sin pre-autenticación requerida 


```python
python3 kerbrute.py -users users.txt -passwords pass.txt -domain dominio.local -t 100
```
El parámetro **-t 100** : sirve para indicar los hilos

#### Impacket
Con impacket, se puede tratar de enumerar los usuarios en un DC. (guest no se cambia, siempre se utiliza "guest")
```bash
impacket-lookupsid guest@<ip> -no-pass
```

### Validar credenciales de dominio

```bash
crackmapexec smb <ip> -u <usuario> -p <contraseña>
```

### Validar winrm

Quizas tengamos opción de lanzar una consola remota, para comprobarlo:
```bash
crackmapexec winrm <ip> -u <usuario> -p <contraseña>
```
