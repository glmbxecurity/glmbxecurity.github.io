En algún directo de twitch, se ve como un usuario del chat, hackea la máquina a la misma vez que el streamer. Al tratarse de la misma máquina, ambos están en el mismo sistema (la maquina comprometida).  

Aquí se puede trolear al streamer, haciendo que todo lo que escribamos en la terminal víctima, se le esté mostrando en directo en la terminal (víctima) del streamer. (ESTO ES SOLO UN EJEMPLO PARA SU COMPRENSIÓN).  

### Primero, que es /dev/pts
En Linux, `/dev/pts` es un directorio especial que se utiliza para gestionar las terminales pseudo (PTY, por sus siglas en inglés). Las terminales pseudo son un mecanismo que permite la comunicación entre procesos, especialmente entre un proceso emulador de terminal y una aplicación que se ejecuta en un sistema Unix-like.

Cuando ejecutas un emulador de terminal, como el terminal de tu sistema operativo, se crea un terminal pseudo para gestionar la comunicación entre el emulador y los procesos que se ejecutan dentro de la terminal. Cada terminal pseudo se representa como un archivo en el directorio `/dev/pts`.

Por ejemplo, si abres varias pestañas en tu terminal, cada una de ellas se asocia con un terminal pseudo diferente en el directorio `/dev/pts`. Estos archivos en `/dev/pts` actúan como interfaces de entrada/salida para las sesiones de terminal.

La denominación específica de los archivos en `/dev/pts` puede variar. Por ejemplo, podrías ver archivos como `pts/0`, `pts/1`, y así sucesivamente, dependiendo de cuántas terminales pseudo estén activas en tu sistema.

En resumen, `/dev/pts` es un directorio que aloja archivos que representan terminales pseudo, utilizados para facilitar la comunicación entre procesos que involucran emuladores de terminal y aplicaciones.

### Intrusión a una terminal

Sabiendo que es /dev/pts, podemos hacer una intrusión a la pseudo terminal de un usuario. Para ello, basta con ejecutar el siguiente comando, **poniendo el número de pts correspondiente a la "víctima".**  
```bash
script -f /dev/pts/1
```

Una vez hecho esto, todo lo que escribamos, la víctima lo estará viendo en tiempo real en su terminal.

#### Conocer el pts de la víctima
```bash
ls /dev/pts
ps aux | grep pts
```
