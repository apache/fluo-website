---
layout: default
title: Releases
permalink: "/release/"
---

## Current

<div class="row">
  <a href="/release/fluo-{{ site.latest_fluo_release }}">
    <div class="col-sm-4 btn btn-info">
      <h3>Fluo {{ site.latest_fluo_release }}</h3>
      <p>Core project containing 'fluo' command to initialize<br> applications, start oracle and worker processes, and<br>manage running applicaitons.</p>
    </div>
  </a>
  <a href="/release/fluo-yarn-{{ site.latest_fluo_yarn_release }}">
    <div class="col-sm-4 btn btn-warning">
      <h3>Fluo YARN {{ site.latest_fluo_yarn_release }}</h3>
      <p>Project containing 'fluo-yarn' command that launches<br>Fluo applications in YARN after they have been<br>initialized using 'fluo' command</p>
    </div>
  </a>
  <a href="/release/fluo-recipes-{{ site.latest_recipes_release }}">
    <div class="col-sm-4 btn btn-success">
      <h3>Fluo Recipes {{ site.latest_recipes_release }}</h3>
      <p>Libraries containing common code that build on the<br>Fluo API to offer complex transactional updates or<br>provide additional utilities<br></p>
    </div>
  </a>
</div>

## Archive

{% assign visible_releases = site.categories.release | where:"draft",false | where:"historical",false %}
{% assign header_year = visible_releases[0].date | date: "%Y" %}
<h3>{{header_year}}</h3>
{% for release in visible_releases %}
  {% assign current_release_year = release.date | date: "%Y" %}
  {% if current_release_year != header_year %}
    {% assign header_year = current_release_year %}
  <hr>
  <h3>{{ header_year }}</h3>
  {% endif %}
  <div class="row" style="margin-top: 15px">
    <div class="col-md-1">{{ release.date | date: "%b %d" }}</div>
    <div class="col-md-10"><a href="{{ site.baseurl }}/release/{{ release.version }}">{{ release.title }}</a></div>
  </div>
{% endfor %}

<hr>

Releases before joining Apache are in [pre-ASF archive](/pre-asf-release/).
