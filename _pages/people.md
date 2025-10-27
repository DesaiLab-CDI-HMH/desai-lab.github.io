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
**Jump to:** [Current Lab Members](#current) · [Alumni](#alumni)
</div>

{%- comment -%}
Current = everyone without alumni: true
Alumni  = everyone with alumni: true
Order within each section controlled by `order` in _data/people.yml
{%- endcomment -%}

{%- assign current = people | where_exp: "p","p.alumni != true" | sort: "order" -%}
{%- if current.size > 0 -%}
<h2 id="current">Current Lab Members</h2>
<div class="grid__wrapper">
  {%- for p in current -%}
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
      {%- assign links_shown = 0 -%}
      {%- if p.email -%}<a href="mailto:{{ p.email }}">Email</a>{%- assign links_shown = 1 -%}{%- endif -%}
      {%- if p.website -%}{% if links_shown %} · {% endif %}<a href="{{ p.website }}">Website</a>{%- assign links_shown = 1 -%}{%- endif -%}
      {%- if p.scholar -%}{% if links_shown %} · {% endif %}<a href="{{ p.scholar }}">Scholar</a>{%- assign links_shown = 1 -%}{%- endif -%}
      {%- if p.github -%}{% if links_shown %} · {% endif %}<a href="{{ p.github }}">GitHub</a>{%- assign links_shown = 1 -%}{%- endif -%}
      {%- if p.linkedin -%}{% if links_shown %} · {% endif %}<a href="{{ p.linkedin }}">LinkedIn</a>{%- assign links_shown = 1 -%}{%- endif -%}
      {%- if p.twitter -%}{% if links_shown %} · {% endif %}<a href="{{ p.twitter }}">Twitter</a>{%- endif -%}
    </p>
  </article>
  {%- endfor -%}
</div>
<hr>
{%- endif -%}

{%- assign alumni = people | where: "alumni", true | sort: "order" -%}
{%- if alumni.size > 0 -%}
<h2 id="alumni">Alumni</h2>
<div class="grid__wrapper">
  {%- for p in alumni -%}
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
      {%- assign links_shown = 0 -%}
      {%- if p.email -%}<a href="mailto:{{ p.email }}">Email</a>{%- assign links_shown = 1 -%}{%- endif -%}
      {%- if p.website -%}{% if links_shown %} · {% endif %}<a href="{{ p.website }}">Website</a>{%- assign links_shown = 1 -%}{%- endif -%}
      {%- if p.scholar -%}{% if links_shown %} · {% endif %}<a href="{{ p.scholar }}">Scholar</a>{%- assign links_shown = 1 -%}{%- endif -%}
      {%- if p.github -%}{% if links_shown %} · {% endif %}<a href="{{ p.github }}">GitHub</a>{%- assign links_shown = 1 -%}{%- endif -%}
      {%- if p.linkedin -%}{% if links_shown %} · {% endif %}<a href="{{ p.linkedin }}">LinkedIn</a>{%- assign links_shown = 1 -%}{%- endif -%}
      {%- if p.twitter -%}{% if links_shown %} · {% endif %}<a href="{{ p.twitter }}">Twitter</a>{%- endif -%}
    </p>
  </article>
  {%- endfor -%}
</div>
{%- endif -%}

<style>
/* polish for avatars and card spacing */
.archive__item-teaser img { width: 100%; height: 100%; object-fit: cover; }
.grid__wrapper { row-gap: 1.5rem; }
.archive__item-title { margin-top: .6rem; }
.page__meta a { white-space: nowrap; }
</style>