---
layout: fluo-doc
title: Fluo 1.0.0-beta-2 Documentation
redirect_from: /docs/1.0.0-beta-2/
version: 1.0.0-beta-2
---

**Fluo is transaction layer that enables incremental processing on big data.**

Fluo is an implementation of [Percolator] built on [Accumulo] that runs in [YARN]. 
It is not recommended for production use yet.

### Getting Started

There are several ways to run Fluo (listed in order of increasing difficulty):

* [quickstart] - Starts a MiniFluo instance that is configured to run a word count application
* [MiniFluo] - Sets up a minimal Fluo instance that writes its data to single directory
* [Uno] - Command-line tool for running Fluo and its dependencies on a single machine
* [Muchos] - Command-line tool that launches an AWS cluster and deploys Fluo and its dependencies to it
* [Production] - Sets up Fluo on a cluster where Accumulo, Hadoop & Zookeeper are running

Except for [quickstart], all above will set up a Fluo application that will be idle unless you
create client & observer code for your application.  You can either [create your own
application][applications] or configure your Fluo application to run an example below:

* [phrasecount] - Computes phrase counts for unique documents
* [Stresso] - Computes the number of unique integers by building bitwise trie

### Implementation

* [Architecture] - Overview of Fluo's architecture
* [Contributing] - Documentation for developers who want to contribute to Fluo
* [Metrics] - Fluo metrics are visible via JMX by default but can be configured to send to Graphite or Ganglia

[Accumulo]: http://accumulo.apache.org
[Percolator]: http://research.google.com/pubs/pub36726.html
[YARN]: http://hadoop.apache.org/docs/r2.5.1/hadoop-yarn/hadoop-yarn-site/YARN.html
[quickstart]: https://github.com/astralway/quickstart
[Uno]: https://github.com/astralway/uno
[Muchos]: https://github.com/astralway/muchos
[phrasecount]: https://github.com/astralway/phrasecount
[Stresso]: https://github.com/astralway/stresso
[MiniFluo]: /docs/fluo/1.0.0-beta-2/mini-fluo-setup/
[Production]: /docs/fluo/1.0.0-beta-2/prod-fluo-setup/
[applications]: /docs/fluo/1.0.0-beta-2/applications/
[Metrics]: /docs/fluo/1.0.0-beta-2/metrics/
[Contributing]: /docs/fluo/1.0.0-beta-2/contributing/
[Architecture]: /docs/fluo/1.0.0-beta-2/architecture/
