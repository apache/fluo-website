---
layout: recipes-doc
title: Apache Spark helper code
version: 1.1.0-incubating
---
Fluo Recipes has some helper code for [Apache Spark][spark].  Most of the helper code is currently
related to bulk importing data into Accumulo.  This is useful for initializing a new Fluo table with
historical data via Spark.  The Spark helper code is found at
[org/apache/fluo/recipes/spark/][sdir].

For information on using Spark to load data into Fluo, check out this [blog post][blog].

If you know of other Spark+Fluo integration code that would be useful, then please consider [opening
an issue](https://github.com/apache/fluo-recipes/issues/new).

[spark]: https://spark.apache.org
[sdir]: {{ site.api_base }}/fluo-recipes-spark/1.1.0-incubating/
[blog]: https://fluo.apache.org/blog/2016/12/22/spark-load/

