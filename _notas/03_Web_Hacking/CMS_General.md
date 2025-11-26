---
title: "CMS General (Drupal, Joomla)"
layout: "single"
category: "Web Hacking"
slug: "web-hacking/cms-general"
date: "2025-11-26"
---

### Drupal
**Enumeración:**
```bash
droopescan scan drupal -u http://target.com
```

**Drupalgeddon2 (CVE-2018-7600):**
RCE crítico en Drupal 7/8.
```bash
use exploit/unix/webapp/drupal_drupalgeddon2
```

### Joomla
**Enumeración:**
```bash
perl joomscan.pl -u http://target.com
```

### Magento
```bash
php magescan.phar scan:all http://target.com
```
