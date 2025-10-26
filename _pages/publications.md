---
layout: single
title: Publications
permalink: /publications/
---

<ul>
{% assign pubs = site.data.publications | sort: "year" | reverse %}
{% for p in pubs %}
  <li>{{ p.citation }}</li>
{% endfor %}
</ul>