---
title: Notas
permalink: /notas/
layout: single
---

{% assign categorias = "Reconocimiento,Servicios comunes,Web Pentesting,Linux Pentesting,Windows Pentesting,Pivoting,Varios,Metodologias" | split: "," %}

{% for cat in categorias %}
**{{ cat }}**

<ul>
  {% assign posts_cat = site.notas | where_exp:"item","item.category == cat" | sort: "title" %}
  {% for post in posts_cat %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

{% endfor %}
