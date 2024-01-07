```bash
script /dev/null -c bash

Ctrl+Z

stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=bash
```