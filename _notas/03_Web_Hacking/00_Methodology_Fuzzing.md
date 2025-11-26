---
title: "Web Methodology & Fuzzing"
layout: "single"
category: "Web Hacking"
slug: "web-hacking/methodology"
date: "2025-11-26"
---

### Checklist Rápido
1.  **Tecnologías:** `whatweb`, Wappalyzer.
2.  **Fuzzing Directorios:** `gobuster`, `feroxbuster`.
3.  **Fuzzing Subdominios:** `wfuzz`, `gobuster vhost`.
4.  **Archivos Sensibles:** `robots.txt`, `sitemap.xml`, `.git/`.
5.  **Parámetros:** Buscar `?id=`, `?file=`, `?url=`.

### Fuzzing Cheatsheet

#### Gobuster (Directorios)
```bash
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt -x php,txt,html
```

#### Wfuzz (Subdominios / VHosts)
```bash
wfuzz -c -f sub-fighter -w subdomains.txt -u http://target.com -H "Host: FUZZ.target.com" --hc 403,404
```

#### Enumeración de Usuarios (Emails)
```bash
nmap -p80 --script http-email-harvest <target>
```

#### Bypass User-Agent
```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" http://target.com
```
