---
title: Apache Fluo Recipes 1.0.0-incubating released
date: 2016-10-28 10:30:00 +0000
version: fluo-recipes-1.0.0-incubating
---

Apache Fluo Recipes builds on the Apache Fluo API to provide libraries of common code for Fluo developers.

Apache Fluo Recipes 1.0.0-incubating is the first release of Fluo Recipes as an Apache project and the third
release for the project.

Below are resources for this release:

 * Download a release tarball and verify by these [procedures] using these [KEYS]

   | [fluo-recipes-1.0.0-incubating-source-release.tar.gz][src-release] | [ASC][src-asc] [MD5][md5] [SHA1][sha1] |

* View the [documentation][docs]
* Read the javadocs: <a href="{{ site.api_base }}/fluo-recipes-core/1.0.0-incubating/" target="_blank">core</a>, <a href="{{ site.api_base }}/fluo-recipes-accumulo/1.0.0-incubating/" target="_blank">accumulo</a>, <a href="{{ site.api_base }}/fluo-recipes-kryo/1.0.0-incubating/" target="_blank">kryo</a>, <a href="{{ site.api_base }}/fluo-recipes-spark/1.0.0-incubating/" target="_blank">spark</a>, <a href="{{ site.api_base }}/fluo-recipes-test/1.0.0-incubating/" target="_blank">test</a>
* Jars are available in [Maven Central][central].

## Changes of interest since last release

* [#112][112] - Avoid allocating collection in AccumuloExporter
* [#107][107] - Added standard way to setup per exporter configuration
* [#102][102] - Simplified Accumulo export queue recipe
* [#92][92] - Added dependency analysis plugin
* [#82][82] - Moved TypeLayer from Fluo API to Fluo Recipes
* [#76][76] - Made compact transient command retry wehn calling compact throws an exception
* [#75][75] - Construct export queue row that falls in bucket
* [#73][73] - Make compact transient sleep for each range
* [#70][70] - Collision Free Map not behaving well when processing backs up
* [#69][69] - Compact transient command has negative impact when processing falls behind
* [#67][67] - Added option to control number of buckets per tablet
* [#50][50] - Renamed Pirto to TableOptimizations

[procedures]: https://www.apache.org/info/verification
[KEYS]: https://www.apache.org/dist/incubator/fluo/KEYS
[src-release]: https://www.apache.org/dyn/closer.lua/incubator/fluo/fluo-recipes/1.0.0-incubating/fluo-recipes-1.0.0-incubating-source-release.tar.gz
[src-asc]: https://www.apache.org/dist/incubator/fluo/fluo-recipes/1.0.0-incubating/fluo-recipes-1.0.0-incubating-source-release.tar.gz.asc
[md5]: https://www.apache.org/dist/incubator/fluo/fluo-recipes/1.0.0-incubating/MD5SUM
[sha1]: https://www.apache.org/dist/incubator/fluo/fluo-recipes/1.0.0-incubating/SHA1SUM
[docs]: /docs/fluo-recipes/1.0.0-incubating
[central]: http://search.maven.org/#search|ga|1|fluo-recipes
[112]: https://github.com/apache/incubator-fluo-recipes/issues/112
[107]: https://github.com/apache/incubator-fluo-recipes/issues/107
[102]: https://github.com/apache/incubator-fluo-recipes/issues/102
[92]: https://github.com/apache/incubator-fluo-recipes/issues/92
[82]: https://github.com/apache/incubator-fluo-recipes/issues/82
[76]: https://github.com/apache/incubator-fluo-recipes/issues/76
[75]: https://github.com/apache/incubator-fluo-recipes/issues/75
[73]: https://github.com/apache/incubator-fluo-recipes/issues/73
[70]: https://github.com/apache/incubator-fluo-recipes/issues/70
[69]: https://github.com/apache/incubator-fluo-recipes/issues/69
[67]: https://github.com/apache/incubator-fluo-recipes/issues/67
[50]: https://github.com/apache/incubator-fluo-recipes/issues/50

