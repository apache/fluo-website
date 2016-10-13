---
layout: page
title: Releases before Apache incubation
permalink: "/pre-asf-release/"
---

<div class="alert alert-danger" role="alert">Please note - This page links to releases made before Apache incubation that are not endorsed by the ASF.</div>

{% for release in site.categories.release %}
{% if release.historical %}
* [{{ release.version }}]({{ site.baseurl }}/release/{{ release.version }}/) - {{ release.date | date_to_string }}
{% endif %}
{% endfor %}


