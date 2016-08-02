---
layout: page
title: Download Fluo
permalink: /pre-asf-download/
---

<div class="alert alert-danger" role="alert">Please note - This is documentation related to non-ASF releases of Fluo.  These releases were made before Apache Fluo became an ASF project and are not endorsed by the ASF.</div>

Releases of Fluo before it became an Apache project can obtained from [Maven
central][dl].   The gpg signatures do not show up in the search results but are
available for download if you add `.asc` to the download URL.

After downloading a release of Apache Fluo, follow these [installation instructions][install] to install Fluo on
a cluster where Accumulo, Hadoop, and Zookeeper are running.

[install]: /docs/fluo/1.0.0-beta-2/prod-fluo-setup/
[dl]: http://search.maven.org/#search|gav|1|g%3A%22io.fluo%22%20AND%20a%3A%22fluo-distribution%22
