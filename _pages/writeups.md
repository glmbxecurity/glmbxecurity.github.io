---
title: Writeups
permalink: /writeups/
layout: single
---

{% assign categorias = "Hackthebox,Tryhackme,Vulnhub,Dockerlabs" | split: "," %}

{% for cat in categorias %}
**{{ cat }}**

<ul>
  {% assign posts_cat = site.writeups | where_exp:"item","item.category == cat" | sort: "title" %}
  {% for post in posts_cat %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

{% endfor %}
