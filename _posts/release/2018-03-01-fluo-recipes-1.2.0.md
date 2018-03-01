---
title: Apache Fluo Recipes 1.2.0 released
date: 2018-03-01 10:30:00 +0000
version: fluo-recipes-1.2.0
draft: true
---

Apache Fluo Recipes builds on the Apache Fluo API to provide libraries of common code for Fluo developers.
The 1.2.0 release is the first release of Fluo Recipes since Fluo graduated from Apache incubation. It has very
few changes from the 1.1.0-incubating release. If you are new to Fluo Recipes, you should use this release. If you
are already using Fluo Recipes 1.1.0-incubating, there is no reason to upgrade immediately.

Below are resources for this release:

* Release artifacts have been pushed to [Maven Central][central]. They can be used by updating your pom.xml:
  ```xml
  <dependency>
    <groupId>org.apache.fluo</groupId>
    <artifactId>fluo-recipes-core</artifactId>
    <version>1.2.0</version>
  </dependency>
  ```
* A source release tarball is available. It can be verified by these [procedures] using these [KEYS]
  * [fluo-recipes-1.2.0-source-release.tar.gz][src-release] - [ASC][src-asc] [MD5][md5] [SHA][sha]
* View the [documentation][docs] for this release
* Read the javadocs: <a href="{{ site.api_base }}/fluo-recipes-core/1.2.0/" target="_blank">core</a>, <a href="{{ site.api_base }}/fluo-recipes-accumulo/1.2.0/" target="_blank">accumulo</a>, <a href="{{ site.api_base }}/fluo-recipes-kryo/1.2.0/" target="_blank">kryo</a>, <a href="{{ site.api_base }}/fluo-recipes-spark/1.2.0/" target="_blank">spark</a>, <a href="{{ site.api_base }}/fluo-recipes-test/1.2.0/" target="_blank">test</a>
* View [changes].

## Notable Changes

### Documentation moved to project website

The [documentation][docs] for Fluo Recipes now lives on the project website. In [#144], it was removed from the Fluo Recipes repo
and moved to Fluo Website repo.

### Updated versions

Fluo Recipes was updated (in [#146]) to build using Fluo 1.2.0 and Accumulo 1.7.3

[#144]: https://github.com/apache/fluo-recipes/pull/144
[#146]: https://github.com/apache/fluo-recipes/pull/146
[procedures]: https://www.apache.org/info/verification
[KEYS]: https://www.apache.org/dist/incubator/fluo/KEYS
[src-release]: https://www.apache.org/dyn/closer.lua/incubator/fluo/fluo-recipes/1.2.0/fluo-recipes-1.2.0-source-release.tar.gz
[src-asc]: https://www.apache.org/dist/incubator/fluo/fluo-recipes/1.2.0/fluo-recipes-1.2.0-source-release.tar.gz.asc
[md5]: https://www.apache.org/dist/incubator/fluo/fluo-recipes/1.2.0/fluo-recipes-1.2.0-source-release.tar.gz.md5
[sha]: https://www.apache.org/dist/incubator/fluo/fluo-recipes/1.2.0/fluo-recipes-1.2.0-source-release.tar.gz.sha
[docs]: /docs/fluo-recipes/1.2/
[central]: http://search.maven.org/#search|ga|1|fluo-recipes
[changes]: https://github.com/apache/incubator-fluo-recipes/milestone/2?closed=1
