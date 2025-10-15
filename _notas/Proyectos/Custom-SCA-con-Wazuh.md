---
title: "Custom Sca Con Wazuh"
layout: single
category: "Proyectos"
slug: "proyectos/custom-sca-con-wazuh"
date: 2025-09-30
---

# Custom SCA con Wazuh
![Logo](https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/312703959/original/4d8c36c4e1ce8111986668ca314a72c298bcee52/setup-and-configure-wazuh-siem.png)
El **Security Configuration Assessment (SCA)** es una herramienta clave para evaluar el cumplimiento de estándares de seguridad como **CIS** o **NIST**, verificando configuraciones como el tiempo de desconexión tras inactividad.

En este artículo, nos enfocaremos en la creación de **SCA personalizados en Wazuh** para cumplir con las directivas de seguridad de las **CCN-STIC**, que evalúan los sistemas según el **Esquema Nacional de Seguridad en España**. Exploraremos cómo desarrollar estos SCA, destacando elementos clave para implementar un sistema de auditoría eficaz y alineado con los requisitos regulatorios, ofreciendo una capa imprescindible de seguridad proactiva para las organizaciones.

![Custom_SCA_Dashboard](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/SOC/custom_sca_dashboard.png)
### Importar las STIC

El primer paso consiste en aplicar la STIC que luego deseamos **monitorear** con el SCA en Wazuh. En este caso, utilizaremos la **570A21 (incremental de dominio)**, diseñada específicamente para servidores **Windows Server 2019 en dominio**. 

Para implementar esta STIC, lo más recomendable es seguir la **guía del CCN-CERT**, ya que está orientada no solo a la aplicación de la normativa, sino también a cómo **monitorear su cumplimiento**.

#### Exportación de configuraciones
Una vez aplicada la STIC al equipo de referencia, el siguiente paso es **exportar las configuraciones** que se han implementado. Este archivo de configuraciones servirá como base para alimentar a Wazuh, permitiéndole monitorear y validar los aspectos clave que nos interesa auditar.

`gpresult /V > C:\rsop_detailed.txt`
### Generar política Wazuh

Con los settings exportados, y siguiendo la documentación oficial de Wazuh ([link](https://documentation.wazuh.com/current/user-manual/capabilities/sec-config-assessment/creating-custom-policies.html)), creamos la plantilla de SCA en formato `.yml`.

Este archivo se llevará al servidor Wazuh. En mi caso, he creado un grupo específico para **Windows Server 2019** (aunque la STIC aplica para cualquier equipo miembro de un dominio). El archivo se ubicará en la siguiente ruta:

**/var/ossec/etc/shared/Windows_Server_2019/ccn_stic_570A21.yml**

```bash
policy:
  id: "ccn_stic_570A21"
  file: "ccn_stic_570A21.yml"
  name: "CCN-STIC-570A21 Incremental Dominio"
  description: "Auditoría de cumplimiento de directivas de seguridad CCN-STIC-570A21 en el dominio."
  references:
    - "https://glmbxecurity.github.io/"

requirements:
  title: "Verificar que el sistema es miembro del dominio"
  description: "Requisitos para aplicar la auditoría."
  condition: all
  rules:
    - 'c:wmic computersystem get domain | findstr /V "WORKGROUP"'

checks:
  - id: 101
    title: "Tiempo máximo de renovación de credenciales (MaxRenewAge)"
    description: "Debe estar configurado en 2 días."
    condition: all
    rules:
      - 'c:secedit /export /cfg C:\\Windows\\Temp\\sc_policy.inf | findstr "MaxRenewAge" -> r:\d+ compare == 2'

  - id: 102
    title: "Duración del bloqueo de cuenta (LockoutDuration)"
    description: "Debe estar configurado en 60 minutos."
    condition: all
    rules:
      - 'c:net accounts | findstr "Lockout duration" -> r:\d+ compare == 60'

  - id: 103
    title: "Duración máxima de contraseña (MaximumPasswordAge)"
    description: "Debe estar configurado en 60 días."
    condition: all
    rules:
      - 'c:net accounts | findstr "Maximum password age" -> r:\d+ compare == 60'

  - id: 104
    title: "Duración mínima de contraseña (MinimumPasswordAge)"
    description: "Debe estar configurado en 2 días."
    condition: all
    rules:
      - 'c:net accounts | findstr "Minimum password age" -> r:\d+ compare == 2'

  - id: 105
    title: "Tiempo de restablecimiento de intentos fallidos (ResetLockoutCount)"
    description: "Debe estar configurado en 30 minutos."
    condition: all
    rules:
      - 'c:net accounts | findstr "Reset account lockout counter" -> r:\d+ compare == 30'

  - id: 106
    title: "Edad máxima de servicio (MaxServiceAge)"
    description: "Debe estar configurado en 360 días."
    condition: all
    rules:
      - 'c:secedit /export /cfg C:\\Windows\\Temp\\sc_policy.inf | findstr "MaxServiceAge" -> r:\d+ compare == 360'

  - id: 107
    title: "Intentos de bloqueo (LockoutBadCount)"
    description: "Debe estar configurado en 8 intentos."
    condition: all
    rules:
      - 'c:net accounts | findstr "Lockout threshold" -> r:\d+ compare == 8'

  - id: 108
    title: "Desfase máximo del reloj (MaxClockSkew)"
    description: "Debe estar configurado en 10 minutos."
    condition: all
    rules:
      - 'c:secedit /export /cfg C:\\Windows\\Temp\\sc_policy.inf | findstr "MaxClockSkew" -> r:\d+ compare == 10'

  - id: 109
    title: "Edad máxima del ticket (MaxTicketAge)"
    description: "Debe estar configurado en 6 horas."
    condition: all
    rules:
      - 'c:secedit /export /cfg C:\\Windows\\Temp\\sc_policy.inf | findstr "MaxTicketAge" -> r:\d+ compare == 6'

  - id: 110
    title: "Historial de contraseñas (PasswordHistorySize)"
    description: "Debe estar configurado en recordar al menos 24 contraseñas."
    condition: all
    rules:
      - 'c:net accounts | findstr "Enforce password history" -> r:\d+ compare == 24'

  - id: 111
    title: "Longitud mínima de la contraseña (MinimumPasswordLength)"
    description: "Debe estar configurado en al menos 10 caracteres."
    condition: all
    rules:
      - 'c:net accounts | findstr "Minimum password length" -> r:\d+ compare >= 10'

```

### Editar Agent.conf
Editaremos el agent.conf del grupo de equipos de Windows Server 2019 desde el manager de wazuh > grupos > ficheros > agent.conf

```bash
# La ruta del .yml es la ruta en la que se encuentra el .yml en el lado del servidor
<agent_config>
  <sca>
    <policies>
      <policy enabled="yes">shared/windows_server2019/ccn_stic_570A21.yml</policy>
    </policies>
  </sca>
</agent_config>
```

### Mover el .yml
Para que el SCA se aplique y realice la auditoría, es necesario mover el archivo `.yml` desde el directorio **shared** al directorio **rulesets/sca** en el lado del cliente (directorio de instalación del agente).

Una forma automatizada de hacerlo es implementar una tarea que detecte cambios en el archivo y lo envíe automáticamente al directorio correspondiente. Para fines de laboratorio, este proceso se puede realizar manualmente.

### Reiniciar y probar cambios
```bash
# Servidor wazuh
systemctl restart wazuh-manager

# Tambien en el servidor (reinicia remotamente los agentes)
/var/ossec/bin/agent_control -R -a

## EN LA MAQUINA CLIENTE MIRAR SI SE ENVIÓ EL YAML EN: (TARDA UN RATO)
C:\Program Files (x86)\ossec-agent\shared\ccn_stic_570a21_incremental_dominio.yml
```

Después de reiniciar, deberíamos poder ver nuestra SCA personalizada en **Configuration assessments**. 

Es probable que inicialmente falle debido a posibles errores en los checks, pero podemos revisar los **Events** para verificar si el archivo se ha cargado correctamente. Una vez ajustados los detalles, se mostrará el cumplimiento de todos los settings configurados.

### Organización | Aplicación | Plantillas CCN-STIC

Las plantillas `.yml` para verificar el cumplimiento de las CCN-STIC se han desarrollado de manera que cada STIC tenga su propio archivo. La forma más eficiente de gestionarlas es creando grupos en Wazuh y asignando a cada uno el archivo `.yml` correspondiente, como se mostró en el tutorial. Ejemplos de grupos:

- Miembros de dominio
- Servidores miembro
- Equipos Windows 10 miembro
- Controlador de dominio
- Servidor Exchange
- ...

Por ejemplo, un servidor **Windows Server 2019** que actúa como controlador de dominio debería pertenecer a los grupos **Miembros de dominio**, **Servidores** y **Controlador de dominio**. Así, los archivos adecuados llegarán al directorio "shared" y solo será necesario moverlos a **rulesets/sca**, ya sea manual o automáticamente.

Basándonos en esta organización, podemos aplicar las STIC correspondientes según los roles o servicios de cada equipo. En la siguiente tabla se detallan algunos ejemplos:
![Tabla_Stics](https://raw.githubusercontent.com/glmbxecurity/glmbxecurity.github.io/refs/heads/main/images/proyectos/SOC/tabla_stics.png)


