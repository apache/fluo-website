---
layout: fluo-doc
title:  Fluo 1.0.0-incubating Documentation
version:  1.0.0-incubating
---

**Apache Fluo lets users make incremental updates to large data sets stored in Apache Accumulo.**

Apache Fluo is an open source implementation of [Percolator][percolator] (which populates
Google's search index) for [Apache Accumulo][accumulo]. Fluo makes it possible to update the results
of a large-scale computation, index, or analytic as new data is discovered.

## Getting Started

* Take the [Fluo Tour][tour] if you are completely new to Fluo.
* Read the [install instructions][install] to install Fluo and start a Fluo application in YARN on a
  cluster where Accumulo, Hadoop & Zookeeper are running. If you need help setting up these
  dependencies, see the [related projects page][related] for external projects that may help.

## Applications

Below are helpful resources for Fluo application developers:

*  [Instructions][apps] for creating Fluo applications
*  [Fluo API][api] javadocs
*  [Fluo Recipes][recipes] is a project that provides common code for Fluo application developers
   implemented using the Fluo API.

## Implementation

*  [Architecture] - Overview of Fluo's architecture
*  [Contributing] - Documentation for developers who want to contribute to Fluo
*  [Metrics] - Fluo metrics are visible via JMX by default but can be configured to send to Graphite
   or Ganglia

**Find documentation for all Fluo releases in the [archive](/docs/)**.

[related]: /related-projects/
[tour]: /tour/
[accumulo]: https://accumulo.apache.org
[percolator]: https://research.google.com/pubs/pub36726.html
[install]: /docs/fluo/1.0.0-incubating/install/
[apps]: /docs/fluo/1.0.0-incubating/applications/
[api]: {{ site.fluo_api_base }}/1.0.0-incubating/
[recipes]: https://github.com/apache/incubator-fluo-recipes
[Metrics]: /docs/fluo/1.0.0-incubating/metrics/
[Contributing]: /docs/fluo/1.0.0-incubating/contributing/
[Architecture]: /docs/fluo/1.0.0-incubating/architecture/
