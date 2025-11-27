---
title: Roadmaps
permalink: /roadmaps/
layout: single
author_profile: true
---

Aquí encontrarás las rutas de aprendizaje y guías que estoy siguiendo.

<div class="entries-list">
  <ul>
    {% for map in site.roadmaps %}
      <li>
        <a href="{{ map.url }}"><strong>{{ map.title }}</strong></a>
        {% if map.excerpt %}<br><small>{{ map.excerpt }}</small>{% endif %}
      </li>
    {% endfor %}
  </ul>
</div>
