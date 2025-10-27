---
layout: single
title: "People"
permalink: /people/
classes: wide
---

<div class="notice--primary" markdown="1">
**Jump to:** [Current Lab Members](#current) · [Alumni](#alumni)
</div>

{%- assign current = site.data.people
    | where_exp: "p", "p.category != 'Alumni'"
    | sort: "order" -%}

## <a id="current"></a>Current Lab Members
<div class="grid__wrapper">
  {%- for p in current -%}
  <article class="archive__item grid__item">
    <div class="archive__item-teaser" style="aspect-ratio:1/1; overflow:hidden;">
      <img src="{{ p.image | default: '/assets/images/team/placeholder.png' }}" alt="{{ p.name | escape }}">
    </div>
    <h3 class="archive__item-title">{{ p.name }}</h3>
    <p class="archive__item-excerpt"><strong>{{ p.role }}</strong></p>
    {%- if p.bio -%}<p class="archive__item-excerpt">{{ p.bio }}</p>{%- endif -%}
    <p class="page__meta">
      {%- if p.email -%}<a href="mailto:{{ p.email }}">Email</a>{%- endif -%}
      {%- if p.website -%}{% if p.email %} · {% endif %}<a href="{{ p.website }}">Website</a>{%- endif -%}
      {%- if p.scholar -%}{% if p.email or p.website %} · {% endif %}<a href="{{ p.scholar }}">Scholar</a>{%- endif -%}
      {%- if p.github -%}{% if p.email or p.website or p.scholar %} · {% endif %}<a href="{{ p.github }}">GitHub</a>{%- endif -%}
      {%- if p.linkedin -%}{% if p.email or p.website or p.scholar or p.github %} · {% endif %}<a href="{{ p.linkedin }}">LinkedIn</a>{%- endif -%}
    </p>
  </article>
  {%- endfor -%}
</div>

<!-- Force the next section to start on a new row even if CSS tries to place it alongside -->
<div style="clear: both;"></div>

<hr style="margin: 2rem 0;" />

{%- assign alumni = site.data.people
    | where: "category", "Alumni"
    | sort: "order" -%}

## <a id="alumni"></a>Alumni
<div class="grid__wrapper">
  {%- for p in alumni -%}
  <article class="archive__item grid__item">
    <div class="archive__item-teaser" style="aspect-ratio:1/1; overflow:hidden;">
      <img src="{{ p.image | default: '/assets/images/team/placeholder.png' }}" alt="{{ p.name | escape }}">
    </div>
    <h3 class="archive__item-title">{{ p.name }}</h3>
    <p class="archive__item-excerpt"><strong>{{ p.role }}</strong></p>
    {%- if p.bio -%}<p class="archive__item-excerpt">{{ p.bio }}</p>{%- endif -%}
    <p class="page__meta">
      {%- if p.email -%}<a href="mailto:{{ p.email }}">Email</a>{%- endif -%}
      {%- if p.website -%}{% if p.email %} · {% endif %}<a href="{{ p.website }}">Website</a>{%- endif -%}
      {%- if p.scholar -%}{% if p.email or p.website %} · {% endif %}<a href="{{ p.scholar }}">Scholar</a>{%- endif -%}
      {%- if p.github -%}{% if p.email or p.website or p.scholar %} · {% endif %}<a href="{{ p.github }}">GitHub</a>{%- endif -%}
      {%- if p.linkedin -%}{% if p.email or p.website or p.scholar or p.github %} · {% endif %}<a href="{{ p.linkedin }}">LinkedIn</a>{%- endif -%}
    </p>
  </article>
  {%- endfor -%}
</div>

<style>
/* small polish */
.archive__item-teaser img { width: 100%; height: 100%; object-fit: cover; }
.grid__wrapper { row-gap: 1.5rem; }
.archive__item-title { margin-top: .6rem; }
.page__meta a { white-space: nowrap; }
</style>