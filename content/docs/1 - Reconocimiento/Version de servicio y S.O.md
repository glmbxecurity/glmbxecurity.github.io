#### version de Linux

```bash
lsb_release -a
```
#### Version de kernel
```bash
uname -r
```

Si tiene página web, se puede probar con whatweb
```bash
whatweb <IP>:puerto
```
> a veces corren servicios, que tienen una interfaz web de administración y no tiene porque ser siempre el 80 o 443. ejemplo: kibana
### Conocer version del servicio con netcat
no siempre se saca con nmap, esta es una alternativa
```bash
nc <ip> <puerto>
```