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

Before starting the tour, you may be wondering how you could use Fluo. A simple
use case shows one possible way to use Fluo: the case of counting words in
unique documents. This could be accomplished by two MapReduce jobs: one job to
get a unique set of documents and a following job to count words. For a large
amount of existing data, running both jobs for a small amount of new data is
inefficient. Fluo enables continuous, quick computations of these two joins as
new data arrives, constantly emitting deltas of word counts.  Anything could
consume the emitted deltas. For example, a query system could be continuously
updated using them. Later in the tour, you can implement this use case.

We recommend following the tour in order. However, all pages are listed below for review.  When on a
tour page, the left and right keys on the keyboard can be used to navigate.  If you have any
questions or suggestions while going through the tour, please contact us.  There are multiple
options for getting in touch : [mailing list, IRC][contact], and [GitHub Issues][issues].  Any
thoughts, solutions, etc  related to this tour can also be tweeted using the hashtag
[#apachefluotour][aft].


{% for p in tour_pages %}
  {% assign doc_url = p | prepend: '/tour/' | append: '/' %}
  {% assign link_to_page = site.pages | where:'url',doc_url | first %}
  1. [{{ link_to_page.title }}]({{ doc_url }})
{% endfor %}

[contact]: /contactus/
[issues]: https://github.com/apache/fluo-website/issues
[aft]: https://twitter.com/hashtag/apachefluotour
