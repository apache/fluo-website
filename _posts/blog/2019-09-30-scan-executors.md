---
title: "How Fluo Leveraged Scan Executors"
date: 2019-09-30 11:50:00 +0000
author: Keith Turner
---

Accumulo 2.0 introduced [Scan Executors][1] giving control over processing of
scans in Accumulo tablet servers. Fluo has a good use case for scan executors,
notification scans.  Fluo worker processes continually scan for notifications
that indicate there is work to do. All workers continually scanning for
notifications can place a lot of load on Accumulo tablet servers which could
negatively impact transactions.  The new scan executor feature provides a way
to limit this load.

Fluo utilizes this feature by [setting scan hints][2] for notification scans
indicating `scan_type=fluo-ntfy`.  These hints are passed to Accumulo tablet
servers and are ignored by default. For these scan types Accumulo could be
configured to either send them to special thread pool and/or prioritize them
differently within a thread pool.  Below is an example of Accumulo shell
commands that setup a special executor for notification scans.

```
config -s tserver.scan.executors.fnotify.threads=1
config -t fluo_table -s table.scan.dispatcher=org.apache.accumulo.core.spi.scan.SimpleScanDispatcher
config -t fluo_table -s table.scan.dispatcher.opts.executor.fluo-ntfy=fnotify
```

The system setting `tserver.scan.executors.fnotify.threads=1` creates a single
threaded scan executor in each tablet server named `fnotify`. The two per table
settings configure a scan dispatcher (the SimpleScanDispatcher is built into
Accumulo) on the fluo table.  The scan dispatcher is configured such that when
a scan hint of `scan_type=fluo-ntfy` is seen it runs on the executor `fnotify`.
All other scans will run on the default executor. This has the effect running
all notification scans on a single dedicated thread in each tablet server.

The above setting were tested in a scenario where 20 Fluo worker were run
against a single tablet server with 20 tablets.  The Fluo stress test was run
with a low ingest rate, resulting in continual notification scanning by the 20
workers.  While the test was running, jstack and top were used to inspect the
tablet server. This inspection revealed that notification scans were all
running in single thread which was using 100% of a single core.  This left all
of the other cores free to process transactions.  Further testing to see how
this impacts throughput is needed. Observing the worker debug logs, all of them
seemed to complete notification scans quickly finding new work.

Fluo took a descriptive approach to using scan hints, where it described what
type of scan was running to Accumulo.  However, Fluo does not care what if
anything Accumulo does with that information.  This allows administrators to
configure Accumulo in many different ways to handle notification scans, without
any changes to Fluo.

For my first pass at using scan executors I tried a prescriptive approach. I
attempted to use scan hints to explictily name an executor for notification
scans.  I realized this would require Fluo configuration to provide the name of
the scan executor. Forcing a user to specify Accumulo and Fluo configuration
was very cumbersome so I abandoned the prescriptive approach.  The descriptive
approach I settled on its place is less cumbersome (it only requires Accumulo
config) and more flexible (it supports executors and/or prioritization instead
of only executors).

At the time of this writing no released version of Fluo supports Accumulo 2.0.
Once Fluo 1.3.0 is released with Accumulo 2.0, Hadoop 3.0, and Java 11 support
it will include support for scan executors.

[1]: https://accumulo.apache.org/docs/2.x/administration/scan-executors
[2]: https://github.com/apache/fluo/blob/57b154e13c5c0877bb565fcabf620aa0f30c9f24/modules/core/src/main/java/org/apache/fluo/core/worker/finder/hash/ScanTask.java#L197

