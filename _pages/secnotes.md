---
layout: archive
title: "Cibersecurity Notes"
permalink: /secnotes/
---
{% assign secnotes_posts = site.posts | where_exp: "post", "post.categories contains 'secnotes'" %}

{% if secnotes_posts == empty %}
  <p>No hay posts todavía en esta categoría.</p>
{% else %}
  <div>
    {% for post in secnotes_posts %}
      <div class="mb-4">
        <a href="{{ post.url }}" class="post-card-title">{{ post.title }}</a>
        <span class="text-small text-gray">{{ post.excerpt }}</span>
      </div>
    {% endfor %}
  </div>
{% endif %}
