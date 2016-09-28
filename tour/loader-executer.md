---
title: Loader Executor
---

Fluo provides a simple mechanism to help load data called the [LoaderExecutor][le].  Loading data
into Fluo requires a transaction.  The LoaderExecutor manages creating , commiting, and retrying
transactions when collisions occur.  It also runs transactions in multiple threads and batches
commit processing of separate transactions for efficiency.  FluoConfiguration provides two methods
for configuring LoaderExecutors [setLoaderQueueSize()][fcqs] and [setLoaderThreads()][fcst].

Objects that implement [Loader] are given to a LoaderExecutor.  The [load()][lm] method will
eventually be called on these objects at which point the passed in transactions can be used to load
data.  When `close()` is called on a LoaderExecutor, it waits for all running and queued work to
finish.

There is no stand alone excercise for the LoaderExecutor.  Hands on experience with it can be
obtained by completing the [word count exercise](/tour/exercise-1/) that is a few pages later in
the tour.

[le]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/LoaderExecutor.html
[Loader]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/Loader.html
[lm]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/Loader.html#load-org.apache.fluo.api.client.TransactionBase-org.apache.fluo.api.client.Loader.Context-
[fcqs]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/config/FluoConfiguration.html#setLoaderQueueSize-int-
[fcst]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/config/FluoConfiguration.html#setLoaderThreads-int-
