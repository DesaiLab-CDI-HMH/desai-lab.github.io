{% assign pubs = site.data.publications | sort: "year" | reverse %}
{% assign grouped = pubs | group_by: "year" %}

{% for group in grouped %}
### {{ group.name }}
<ul class="pub-list">
  {% for p in group.items %}
  <li>{{ p.citation_nature }}</li>
  {% endfor %}
</ul>
{% endfor %}