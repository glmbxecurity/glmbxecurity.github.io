---
title: "Pivoting Basics"
layout: "single"
category: "Pivoting"
slug: "pivoting/pivoting-basics"
date: "2025-09-30"
---

### Enrutar tráfico
Cuando tenemos una 3ª máquina conectada a una víctima ya comprometida, para lanzar escaneos, pivotar, etc, necesitamos enrutar el tráfico, ejemplo tenemos:

* *KALI --> VM 1 --> VM 2** 
* Kali -> 10.0.0.1
* VM1 -> ETH0: 10.0.0.2
	* -> ETH1: 45.0.0.1
* VM2 -> 45.0.0.2

Teniendo una sesión de meterpreter con la **VM1**, lanzamos el comando:
```bash
autoroute -s 45.0.0.1
### Mandamos esta sesion a segundo plano para poder lanzar un escaneo sobre la nueva víctima.
background
```

