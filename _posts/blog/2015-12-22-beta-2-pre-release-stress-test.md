---
title:  "Beta 2 pre-release stress test"
date:   2015-12-22 15:30:00
redirect_from: /beta-2-pre-release-stress-test/
---

In preperation for a beta 2 release, the [stress test][3] was run again on EC2.
The test went well outperforming the [first stress test][1] and [beta-1 stress
test][2]. 

For this test run, initially ~1 billion random integers were generated and
loaded into Fluo via map reduce.  After that, 1 million random integers were
repeatedly loaded 20 times, sleeping 10 minutes between loads.  After
everything finished, the test was a success. The number of unique integers
computed independently by MapReduce matched the number computed by Fluo.  Both
computed 1,019,481,332 unique integers.

The test took a total of 7 hours 30 minutes and 30 seconds.  Over this time
period 61.7 million NodeObserver and 20 million NodeLoader transactions were
executed.  The average rate of transactions per second for the entire test was
2,968 tansactions per second.  At the conclusion of the test, the stress table
had 3.87 billion entries.

The test was run with the following environment.

 * 18 m3.xlarge worker nodes
 * 18 Fluo workers, each having had 4G memory and 128 threads
 * 18 Map reduce load task, each with 32 threads
 * 18 Tablet servers, each with 3G (1.5G for data cache, .5G for index cache, and .5G for in memory map)
 * Fluo built from [c4789b3][4]
 * Fluo stress built from [32edaf9][5]
 * Accumulo 1.8.0-SNAPSHOT with [ACCUMULO-4066][6] patch.

Grafana plots
-------------

An exciting new development in the Fluo eco-system for beta-2 is the
utilization of Grafana and InfluxDB to plot metrics.  Also metrics
configuration was simplified making it possible to report metrics from Map
Reduce and Spark. In the plots below we can see metrics from the load
transactions executing in Map Reduce.  In previous test, this was not visible,
being able to see it now is really useful.

![Grafana long run](/resources/blog/stress_3/grafana-1.png)

Notifications were building up during the test. A better method than sleeping
between loads, as mentioned in [fluo-io/fluo-stress#30][7], is still needed.

Short runs
----------

Before starting the long run, a few short runs loading 1 million few times were
done with an empty table.

![Grafana short run](/resources/blog/stress_3/grafana-2.png)

Further testing
---------------

A long run of webindex will also be run on EC2 before releasing beta-2.

[1]: /blog/2014/12/30/stress-test-long-run/
[2]: /release-notes/1.0.0-beta-1/
[3]: https://github.com/fluo-io/fluo-stress
[4]: https://github.com/fluo-io/fluo/commit/c4789b3100092683b37c57c48ddd87993e84972c
[5]: https://github.com/fluo-io/fluo-stress/commit/32edaf91138bb13b442632262c23e7f13f8fb17c
[6]: https://issues.apache.org/jira/browse/ACCUMULO-4066
[7]: https://github.com/fluo-io/fluo-stress/issues/30

