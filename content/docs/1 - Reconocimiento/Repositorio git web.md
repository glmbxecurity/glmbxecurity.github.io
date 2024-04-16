Cuando encontramos un sitio web construido con git, es posible que se detecte el conocido directorio **.git**, en ese caso se puede tratar de analizar ya que podríamos encontrar información interesante en el código, comentarios, accesos a bbdd, credenciales etc.

### Dumpear repositorio git
Dumpear / clonar repositorio git de una web es tan sencillo como utilizar la herramienta [git-dumper](https://github.com/arthaud/git-dumper) de la siguiente manera:
```bash
git-dumper http://ip/ruta_al_/.git <ruta donde queremos guardar>
```

### Analizar la información
* con ```git log```, podemos ver los comits.
* con ```git show```, seguido de los primeros digitos del commit, podemos ver los cambios en el código.
