---
layout: page
title: Documentation
---

For a general overview of Fluo, take the [Fluo tour](/tour/).

[Apache Fluo] and [Apache Fluo Recipes] have seperate documentation as they are different repositories with their own release cycle.

## Apache Fluo

Starting with 1.0.0-incubating, Apache Fluo will follow [semver](http://semver.org/) for all API
changes.  The API consist of evertyhing under the org.apache.fluo.api package.  Code outside of this
package can change at any time.  If your project is using Fluo code that falls outside of the API,
then consider [initiating a discussion](/getinvolved/) about adding it to the API.

Last release was `{{ site.latest_fluo_release }}` made on {{ site.latest_fluo_release_date }}.

* Documentation - [Latest][fluo-docs-latest] \| [Archive][fluo-docs-archive]
* API - [Latest][fluo-api-latest] \| [Archive][fluo-api-archive]
* Release summary -  [Latest][fluo-sum-latest] \| [Archive][fluo-sum-archive]
* Release notes - [Latest][fluo-notes-latest] \| [Archive][fluo-notes-archive]

## Apache Fluo Recipes

The first release of Apache Fluo Recipes has not been made yet.

## Pre Apache Documentation

Documentation about releases made before Apache Fluo entered incubation at Apache has been moved [here](pre-asf)

[fluo-docs-latest]: /docs/fluo/{{ site.latest_fluo_release }}/
[fluo-api-latest]: /apidocs/fluo/{{ site.latest_fluo_release }}/
[fluo-sum-latest]: /release-summaries/{{ site.latest_fluo_release }}/
[fluo-notes-latest]: /release-notes/{{ site.latest_fluo_release }}/
[Apache Fluo]: https://github.com/apache/fluo
[Apache Fluo Recipes]: https://github.com/apache/fluo-recipes
[fluo-docs-archive]: /docs/fluo/
[fluo-api-archive]: /apidocs/fluo/
[fluo-sum-archive]: /release-summaries/
[fluo-notes-archive]: /release-notes/
