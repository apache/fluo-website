---
layout: page
title: Pre-ASF releases
permalink: "/pre-asf-release/"
---

<div class="alert alert-danger" role="alert">Please note - This page links to non-ASF releases. These releases were made before Apache Fluo became an ASF project and are not endorsed by the ASF.</div>

{% for release in site.categories.release %}
{% if release.historical %}
* [{{ release.version }}]({{ site.baseurl }}/release/{{ release.version }}/) - {{ release.date | date_to_string }}
{% endif %}
{% endfor %}


