---
layout: page
title: Quickstart
permalink: /quickstart/
---

This quickstart example runs a Fluo application that counts the number of times each word occurs
in documents loaded into Fluo.  In order to run this example, you will need [Git], [Java], and 
[Maven] installed.

First, clone the [fluo-quickstart] repo:

{% highlight bash %}
git clone https://github.com/fluo-io/fluo-quickstart.git
{% endhighlight %}

Next, build [fluo-quickstart] which will import all jars needed to run Fluo:

{% highlight bash %}
cd fluo-quickstart
mvn package
{% endhighlight %}

Finally, run the Fluo application using Maven:

{% highlight bash %}
mvn exec:java -Dexec.mainClass=io.fluo.quickstart.Main -Dexec.cleanupDaemonThreads=false
{% endhighlight %}

The quickstart [Main] class does all of the heavy lifting.  It starts a local Fluo instance (called MiniFluo), 
adds documents, waits for the [DocumentObserver] to finish processing all documents, and then prints 
out the word counts of the loaded documents.  It finally shutdowns MiniFluo before exiting. 

This example is intentionally not comprehensive to keep it short and provide you an opportunity to experiment.
Further improvements are suggested in the source code comments of [Main] & [DocumentObserver] if you are
interested. For a more comprehensive Fluo application, see the [phrasecount] example.

[Git]: http://git-scm.com/
[Java]: https://www.oracle.com/java/index.html
[Maven]: http://maven.apache.org/
[fluo-quickstart]: https://github.com/fluo-io/fluo-quickstart
[Main]: https://github.com/fluo-io/fluo-quickstart/blob/master/src/main/java/io/fluo/quickstart/Main.java
[DocumentObserver]: https://github.com/fluo-io/fluo-quickstart/blob/master/src/main/java/io/fluo/quickstart/DocumentObserver.java
[phrasecount]: https://github.com/fluo-io/phrasecount
