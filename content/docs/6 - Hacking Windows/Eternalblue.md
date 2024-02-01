Vulnerabilidad que afecta a sistemas operativos windows relativamente antiguos, (Windows 7, Windows server 2008), que nos permite ejecución remota de comandos. el CVE: **CVE-2017-0143** y **MS17-010** 

Al detectar esto con nmap, se puede llegar a explotar de diferentes maneras:
```bash
nmap 10.10.10.4 --script "vuln" -p 445
```

### Método 1 (Metasploit)

Abrimos metasploit, buscamos el exploit y lo "usamos". Completamos todos los campos necesarios que nos pide el exploit y el payload, y lo lanzamos, "run". 


