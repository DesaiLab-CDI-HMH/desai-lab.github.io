---
layout: single
title: "People"
permalink: /people/
classes: wide
---

{%- assign people = site.data.people | default: empty -%}
{%- if people == empty -%}
<p><em>No people found. Add entries to <code>_data/people.yml</code>.</em></p>
{%- endif -%}

<!-- Quick jump links -->
<div class="notice--primary" markdown="1">
**Jump to:** [Current Lab Members] · [Alumni](#alumni)
</div>

{%- assign sections = "PI,Staff,Postdoc,Graduate,Undergraduate,Alumni" | split: "," -%}
{%- for section in sections -%}
  {%- assign group = people | where: "category", section | sort: "order" -%}
  {%- if group.size > 0 -%}
  <h2 id="{{ section | downcase }}">{{ section }}</h2>
  <div class="grid__wrapper">
    {%- for p in group -%}
    <article class="archive__item grid__item">
      <div class="archive__item-teaser" style="aspect-ratio:1/1; overflow:hidden;">
        <img src="{{ p.image | default: '/assets/images/team/placeholder.png' }}" alt="{{ p.name | escape }}">
      </div>
      <h3 class="archive__item-title">{{ p.name }}</h3>
      <p class="archive__item-excerpt"><strong>{{ p.role }}</strong></p>
      {%- if p.bio -%}
      <p class="archive__item-excerpt">{{ p.bio }}</p>
      {%- endif -%}
      <p class="page__meta">
        {%- if p.email -%}<a href="mailto:{{ p.email }}">Email</a>{%- endif -%}
        {%- if p.website -%}{% if p.email %} · {% endif %}<a href="{{ p.website }}">Website</a>{%- endif -%}
        {%- if p.scholar -%}{% if p.email or p.website %} · {% endif %}<a href="{{ p.scholar }}">Scholar</a>{%- endif -%}
        {%- if p.github -%}{% if p.email or p.website or p.scholar %} · {% endif %}<a href="{{ p.github }}">GitHub</a>{%- endif -%}
        {%- if p.twitter -%}{% if p.email or p.website or p.scholar or p.github %} · {% endif %}<a href="{{ p.twitter }}">Twitter</a>{%- endif -%}
      </p>
    </article>
    {%- endfor -%}
  </div>
  <hr>
  {%- endif -%}
{%- endfor -%}

<style>
/* optional: subtle polish for avatars and card spacing */
.archive__item-teaser img { width: 100%; height: 100%; object-fit: cover; }
.grid__wrapper { row-gap: 1.5rem; }
.archive__item-title { margin-top: .6rem; }
.page__meta a { white-space: nowrap; }
</style>