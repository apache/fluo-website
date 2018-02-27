---
layout: page
title: Releases
permalink: "/release/"
---

Apache Fluo has several projects that are released separately on their own schedule.

{% for release in site.categories.release %}
{% unless release.historical or release.draft %}
* [{{ release.version }}]({{ site.baseurl }}/release/{{ release.version }}/) - {{ release.date | date_to_string }}
{% endunless %}
{% endfor %}

Releases before joining Apache have been [archived](/pre-asf-release/).
