---
layout: page
title: Download Apache Fluo
permalink: /download/
---

Tarball distributions of Apache Fluo will be available on this page after its first release as an Apache project.

Prior releases of Fluo before it became an Apache project can be found on [GitHub].

After downloading a release of Apache Fluo, follow these [installation instructions][install] to install Fluo on
a cluster where Accumulo, Hadoop, and Zookeeper are running.

External (non-ASF) projects exist to automate the installation of Apache Fluo and its dependencies:

* [fluo-dev] - Sets up Fluo and its dependencies on a single machine for development
* [Zetten] - Sets up Fluo and its dependencies on a cluster (optionally launched in Amazon EC2)

[GitHub]: https://github.com/apache/fluo/releases
[install]: /docs/fluo/{{ site.latest_fluo_release}}/prod-fluo-setup/
[fluo-dev]: https://github.com/fluo-io/fluo-dev
[Zetten]: https://github.com/fluo-io/zetten
