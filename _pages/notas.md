---
title: Notas
permalink: /notas/
layout: single
author_profile: true
---

{% comment %} 
Lista de categorías en el ORDEN que quieres que aparezcan. 
Deben coincidir EXACTAMENTE con los nombres del script de Python (CATEGORY_MAP).
{% endcomment %}

{% assign categorias_ordenadas = "Setup,Reconocimiento,Servicios,Web Hacking,Active Directory,Shells,Linux PrivEsc,Windows PrivEsc,Criptografia,Pivoting,Proyectos,Writeups" | split: "," %}

<div class="entries-list">
{% for cat_name in categorias_ordenadas %}

  {% comment %} Buscamos posts que tengan esta categoría exacta {% endcomment %}
  {% assign posts_cat = site.notas | where:"category", cat_name | sort: "title" %}

  {% if posts_cat.size > 0 %}
    <h2 id="{{ cat_name | slugify }}">{{ cat_name }}</h2>
    <ul>
      {% for post in posts_cat %}
        <li>
            <a href="{{ post.url }}">{{ post.title }}</a>
        </li>
      {% endfor %}
    </ul>
    <hr>
  {% endif %}

{% endfor %}
</div>
