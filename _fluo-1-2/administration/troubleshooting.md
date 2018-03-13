---
title: Troubleshooting
category: administration
order: 7
---

Steps for troubleshooting problems with Fluo applications.

## Fluo application stops processing data

1. Confirm that your application is running with the expected number of workers. 
    ```bash
    $ fluo list
    Fluo instance (localhost/fluo) contains 1 application(s)

    Application     Status     # Workers
    -----------     ------     ---------
    webindex        RUNNING        3
    ```
   Look for errors in the logs of any oracle or worker that has died.

1. Run the `fluo wait` command to see if you application is processing notifications. 
    ```bash
    $ fluo wait -a webindex
    [command.FluoWait] INFO : The wait command will exit when all notifications are processed
    [command.FluoWait] INFO : 140 notifications are still outstanding.  Will try again in 10 seconds...
    [command.FluoWait] INFO : 140 notifications are still outstanding.  Will try again in 10 seconds...
    [command.FluoWait] INFO : 140 notifications are still outstanding.  Will try again in 10 seconds...
    [command.FluoWait] INFO : 96 notifications are still outstanding.  Will try again in 10 seconds...
    [command.FluoWait] INFO : 70 notifications are still outstanding.  Will try again in 10 seconds...
    [command.FluoWait] INFO : 31 notifications are still outstanding.  Will try again in 10 seconds...
    [command.FluoWait] INFO : All processing has finished!
    ```
   The number of notifications will increase as data is added to the application but they should eventually decrease
   to zero and processing should finish.

1. Look for errors or exceptions in the logs of all oracle and worker processes. Processing can stop if all threads
   in a worker process were consumed by exceptions thrown in Fluo application's observer code. These exceptions
   are often due to parsing issues or corner cases not seen during development or using small data sets.

1. If you are using a cluster manager (i.e Marathon, YARN etc) to run your Fluo application, look for errors in the logs of
   your cluster manager or application manager.  Below are some common errors: 

    * Cluster managers sometimes fail to start all process of Fluo application due to lack of container slots or resources (CPU, memory, etc).
      This can be fixed by giving more resources to your cluster manager or decrease the number/resources of Fluo workers.
    * Cluster managers can kill Fluo processes if they use too much memory. This can be fixed by allocating more memory to your workers.

1. Run [jstack] to get stack traces of threads in your Fluo application processes and look for any stuck threads.

1. Consider configuring your Fluo application to [report metrics][metrics] so that they are viewable in Grafana/InfluxDB. Metrics
   can are helpfu in debugging performance issues.

If you are still having trouble, feel free to email `dev@fluo.apache.org` for help.

[jstack]: https://docs.oracle.com/javase/8/docs/technotes/tools/unix/jstack.html
[metrics]: {{ page.docs_base }}/administration/metrics
