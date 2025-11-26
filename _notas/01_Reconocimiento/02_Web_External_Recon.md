---
title: "Web & External Recon"
layout: "single"
category: "Reconocimiento"
slug: "reconocimiento/web-external-recon"
date: "2025-11-26"
---

Guía para reconocimiento externo, enumeración de dominios, OSINT y fingerprinting web.

## 1. OSINT & Google Dorks (Pasivo)

### Google Dorks Cheatsheet
Utiliza `site:target.com` combinado con:
* `ext:pdf` / `ext:docx` / `ext:xlsx` (Ficheros expuestos)
* `inurl:admin` / `intitle:"index of"` (Paneles y Directorios)
* `intext:"password" filetype:log` (Credenciales en logs)
* `inurl:conf` / `inurl:env` (Archivos de configuración)

### Herramientas OSINT
* **[TheHarvester](https://github.com/laramies/theHarvester):** Emails, subdominios y IPs.
  ```bash
  theHarvester -d target.com -b google,bing,linkedin,dnsdumpster
  ```
* **[Phonebook.cz](https://phonebook.cz):** Buenísimo para emails y dominios.
* **[HaveIBeenPwned](https://haveibeenpwned.com):** Verificar brechas de correos encontrados.
* **[WaybackMachine](https://archive.org/web/):** Buscar versiones antiguas de la web, archivos JS viejos o endpoints ocultos.

---

## 2. Enumeración DNS y Subdominios (Activo)

### Transferencia de Zona (AXFR)
Si el servidor DNS está mal configurado, te dará todos los subdominios.
```bash
dig axfr @<IP_DNS> dominio.com
host -l dominio.com <IP_DNS>
```

### Fuerza Bruta de Subdominios
```bash
# Gobuster DNS (Muy rápido)
gobuster dns -d dominio.com -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t 20

# Wfuzz (Subdominios mediante Host Header - Virtual Hosting)
wfuzz -c -f sub-fighter -w subdomains.txt -u [http://target.com](http://target.com) -H "Host: FUZZ.target.com" --hc 403,404
```

### Otras herramientas DNS
* **Dnsenum:** `dnsenum target.com`
* **Fierce:** `fierce --domain target.com`

---

## 3. Reconocimiento Web (Fingerprinting)

### Identificación de Tecnologías
* **Wappalyzer / BuiltWith:** Extensiones de navegador.
* **WhatWeb:** `whatweb -a 3 http://target.com`
* **WAFw00f:** Detectar Firewall de Aplicación Web (Cloudflare, Imperva, ModSecurity).
  ```bash
  wafw00f [http://target.com](http://target.com) -a
  ```

### Archivos de Interés
Siempre revisa manualmente:
* `/robots.txt`
* `/sitemap.xml`
* `/security.txt`
* `/scaneo_home_page` (Ctrl+U y busca comentarios ``)

### Clonado de Web (Análisis Local)
```bash
httrack [http://target.com](http://target.com) -O /tmp/web_clone
```
