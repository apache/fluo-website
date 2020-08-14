---
layout: page
title: Related Projects
permalink: /related-projects/
---

This page list external projects that build on Apache Fluo and may be useful.
These projects are not necessarily affiliated with or endorsed by the 
[Apache Software Foundation][asf]. If you would like to add a project to this 
list, please open an issue or submit a pull request [on GitHub][web-ghr].

### Projects Using Fluo

* [Apache Rya][Rya] - Uses Fluo to keep precomputed joins update to date as new data arrives.

### Tools for running Apache Fluo

* [Uno] - Runs Apache Hadoop+Zookeeper+Accumulo+Fluo on a single machine for development and testing.
* [Muchos] - Deploys Apache Hadoop+Zookeeper+Accumulo+Fluo to a cluster (optionally launched in Amazon EC2) for development and testing.

### Example Fluo applications

* [Phrasecount] - Example Apache Fluo application that counts phrases in documents
* [Mixer] - Prototype showing how to use Apache Fluo to continuously merge multiple large graphs into a single derived one.
* [Jaccard] - Example Apache Fluo application that computes and indexes the Jaccard between all pairs in a bipartite graph.
* [Webindex] - Apache Fluo application that creates web index using Common Crawl data
* [Stresso] - An example application designed to stress Apache Fluo

[asf]: https://www.apache.org/
[Fluo]: https://github.com/apache/fluo
[Fluo Recipes]: https://github.com/apache/fluo-recipes
[Muchos]: https://github.com/apache/fluo-muchos
[Uno]: https://github.com/apache/fluo-uno
[Webindex]: https://github.com/apache/fluo-examples/tree/main/webindex
[Stresso]: https://github.com/apache/fluo-examples/tree/main/stresso
[Phrasecount]: https://github.com/apache/fluo-examples/tree/main/phrasecount
[Jaccard]: https://github.com/keith-turner/jaccard
[web-ghr]: https://github.com/apache/fluo-website
[Rya]: https://rya.apache.org
[Mixer]: https://github.com/keith-turner/mixer
