---
layout: single
title: "Publications"
permalink: /publications/
---

{% assign pubs = site.data.publications | sort: "year" | reverse %}
{% assign years = pubs | map: "year" | uniq %}

{% for y in years %}
## {{ y }}
<ul class="bibliography">
  {% assign group = pubs | where: "year", y %}
  {% for p in group %}
  <li>
    {% if p.authors %}{{ p.authors | join: ", " }}. {% endif %}
    <strong>{{ p.title }}</strong>.
    {% if p.journal %}<em>{{ p.journal }}</em>{% endif %}{% if p.volume %} {{ p.volume }}{% endif %}{% if p.issue %}({{ p.issue }}){% endif %}{% if p.pages %}:{{ p.pages }}{% endif %}{% if p.year %} ({{ p.year }}){% endif %}.
    {% if p.doi %} <a href="https://doi.org/{{ p.doi }}">doi:{{ p.doi }}</a>.{% elsif p.url %} <a href="{{ p.url }}">Link</a>.{% endif %}
  </li>
  {% endfor %}
</ul>
{% endfor %}