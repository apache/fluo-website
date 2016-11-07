---
layout: page
title: Fluo Tour
permalink: /tour/
---

{% assign tour_pages = site.data.tour.docs %}
{% assign first_url = tour_pages[0] | prepend: '/tour/' | append: '/' %}
{% assign first_page = site.pages | where:'url',first_url | first %}

Welcome to the Fluo tour!  The tour offers a hands on introduction to Fluo, broken down into
independent steps and an exercise.  The exercise gives you a chance to apply what
you have learned.   The tour starts by introducing Fluo's [{{ first_page.title }}]({{ first_url }}).

We recommend following the tour in order. However, all pages are listed below for review.  When on a
tour page, the left and right keys on the keyboard can be used to navigate.  If you have any
questions or suggestions while going through the tour, please let us know.  There are multiple
options for getting in touch : [mailing list, IRC][contact], and [Github Issues][issues].  Any
thoughts, solutions, etc  related to this tour can also be tweeted using the hashtag
[#apachefluotour][aft].


{% for p in tour_pages %}
  {% assign doc_url = p | prepend: '/tour/' | append: '/' %}
  {% assign link_to_page = site.pages | where:'url',doc_url | first %}
  1. [{{ link_to_page.title }}]({{ doc_url }})
{% endfor %}

[contact]: /getinvolved/
[issues]: https://github.com/apache/incubator-fluo-website/issues
[aft]: https://twitter.com/hashtag/apachefluotour
