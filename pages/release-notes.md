---
layout: page
title: Release Notes
permalink: "/release-notes/"
---

#### Apache Fluo release notes

{% for release in site.categories.release-notes %}
{% unless release.historical %}
* [{{ release.version }}]({{ site.baseurl }}/release-notes/{{ release.version }}/) - {{ release.date | date_to_string }}
{% endunless %}
{% endfor %}

#### Release notes before Apache

{% for release in site.categories.release-notes %}
{% if release.historical %}
* [{{ release.version }}]({{ site.baseurl }}/release-notes/{{ release.version }}/) - {{ release.date | date_to_string }}
{% endif %}
{% endfor %}
