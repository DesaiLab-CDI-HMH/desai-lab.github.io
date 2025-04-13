---
layout: single
title: "Publications"
permalink: /publications/
author_profile: true
---

{% for paper in site.data.publications %}
- **{{ paper.title }}**  
  {{ paper.authors }}. _{{ paper.venue }}_ ({{ paper.year }})  
  {% if paper.link %}[PDF]({{ paper.link }}){% endif %}
{% endfor %}

