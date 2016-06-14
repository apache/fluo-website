---
layout: page
title: Fluo Release Notes Archive
permalink: "/release-notes/"
---

Below are the release notes for all Fluo releases:

{% for release in site.categories.release-notes %}
* [{{ release.version }}]({{ site.baseurl }}/release-notes/{{ release.version }}/) - {{ release.date | date_to_string }}
{% endfor %}
