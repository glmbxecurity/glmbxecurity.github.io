---
title: Writeups
permalink: /writeups/
layout: single
---

{% assign categorias = "eJPT,eCPPT,OSCP" | split: "," %}

{% for cat in categorias %}
  
  <h2>{{ cat }}</h2>
  <ul>
    {% assign hay_posts = false %}
    
    {% comment %} 
      Recorremos la colección 'site.writeups' (la carpeta _writeups) 
    {% endcomment %}
    {% assign writeups_ordenados = site.writeups | sort: "title" %}
    
    {% for post in writeups_ordenados %}
      {% comment %} 
        Usamos 'contains' porque en tu post definiste categories como una lista 
      {% endcomment %}
      {% if post.categories contains cat %}
        <li>
          <a href="{{ post.url }}">{{ post.title }}</a>
          <small style="color: #888;">({{ post.date | date: "%Y-%m-%d" }})</small>
        </li>
        {% assign hay_posts = true %}
      {% endif %}
    {% endfor %}
    
    {% if hay_posts == false %}
      <li><em>No hay writeups en esta categoría aún.</em></li>
    {% endif %}
  </ul>

{% endfor %}
