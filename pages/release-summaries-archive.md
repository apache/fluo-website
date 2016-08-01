---
layout: page
title: Release Summaries Archive
permalink: "/release-summaries/"
---

Apache Fluo release summaries:

{% for release in site.categories.release-summaries %}
{% unless release.historical %}
* [{{ release.version }}]({{ site.baseurl }}/release-summaries/{{ release.version }}/) - {{ release.date | date_to_string }}
{% endunless %}
{% endfor %}

Fluo release summaries before Apache incubation:

{% for release in site.categories.release-summaries %}
{% if release.historical %}
* [{{ release.version }}]({{ site.baseurl }}/release-summaries/{{ release.version }}/) - {{ release.date | date_to_string }}
{% endif %}
{% endfor %}


