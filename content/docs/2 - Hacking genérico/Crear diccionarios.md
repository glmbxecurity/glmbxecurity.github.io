### CUPP
Para crear un diccionario para fuerza bruta, con cupp se puede hacer de manera interactiva, y nos pedirá cosas tipo nombre,apellido, nombre de mascota, fecha nacimiento, etc.
```bash
cupp -i
```

### CEWL
crear diccionario a través de la info encontrada en una web, con palabras clave y términos interesantes. lo ideal es hacer fuzzing y pasarle a la herramienta varios directorios/ficheros de la web.
```bash
cewl http://<ip> -w <diccionario_a_exportar1>
cewl http://<ip>/homework -w <diccionario_a_exportar2>
cewl http://<ip>/important -w <diccionario_a_exportar3>

###luego juntamos los ficheros en uno
cat diccionario* > final_diccionario
```