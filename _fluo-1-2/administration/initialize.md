---
title: Initialize Application
category: administration
order: 1
---

## Overview

Before a Fluo Application can run, it must be initialized.  Below is an overview of what
initialization does and some of the properties that may be set for initialization.

 * **Initialize ZooKeeper** - Each application has its own area in ZooKeeper used for configuration,
   Oracle state, and worker coordination. All properties, except `fluo.connections.*`, are copied
   into ZooKeeper. For example, if `fluo.worker.num.threads=128` was set, then when a worker process
   starts it will read this from ZooKeeper.
 * **Copy Observer jars to DFS** - Fluo workers processes need the jars containing observers. These
   are provided in one of the following ways.
   * Set the property `fluo.observer.init.dir` to a local directory containing observer jars. The
     jars in this directory are copied to DFS under `<fluo.dfs.root>/<app name>`. When a worker is
     started, the jars are pulled from DFS and added to its classpath.
   * Set the property `fluo.observer.jars.url` to a directory in DFS containing observer jars.  No
     copying is done. When a worker is started, the jars are pulled from this location and added to
     its classpath.
   * Do not set any of the properties above and have the mechanism that starts the worker process
     add the needed jars to the classpath.
 * **Create Accumulo table** - Each Fluo application creates and configures an Accumulo table. The
   `fluo.accumulo.*` properties determine which Accumulo instance is used. For performance reasons,
   Fluo runs its own code in Accumulo tablet servers. Fluo attempts to copy Fluo jars into DFS and
   configure Accumulo to use them. Fluo first checks the property `fluo.accumulo.jars` and if set,
   copies the jars listed there. If that property is not set, then Fluo looks on the classpath to
   find jars. Jars are copied to a location under `<fluo.dfs.root>/<app name>`.

## Instructions

Below are the steps to initialize an application from the command line. It is also possible to
initialize an application using Fluo's Java API.

1. Create a copy of [fluo-app.properties] for your Fluo application. 

        cp $FLUO_HOME/conf/fluo-app.properties /path/to/myapp/fluo-app.properties

2. Edit your copy of [fluo-app.properties] and make sure to set the following:

    * Class name of your ObserverProvider
    * Paths to your Fluo observer jars
    * Accumulo configuration
    * DFS configuration

   When configuring the observer section of fluo-app.properties, you can configure your instance for the
   [phrasecount] application if you have not created your own application. See the [phrasecount]
   example for instructions. You can also choose not to configure any observers but your workers will
   be idle when started.

3. Run the command below to initialize your Fluo application. Change `myapp` to your application name:

        fluo init myapp /path/to/myapp/fluo-app.properties

   A Fluo application only needs to be initialized once. After initialization, the Fluo application
   name is used to start/stop the application and scan the Fluo table.

4. Run `fluo list` which connects to Fluo and lists applications to verify initialization.

5. Run `fluo config myapp` to see what configuration is stored in ZooKeeper.

## Next Steps

Run your Fluo application using one of the methods below:

* [Run Fluo processes][process]
* [Run Fluo in YARN][yarn]
* [Run Fluo in Docker][docker] which enables running in Mesos and Kubernetes

Also, learn how to [manage Fluo applications][manage].

[fluo-app.properties]: {{ page.github_base}}/modules/distribution/src/main/config/fluo-app.properties
[fluo-conn.properties]: {{ page.github_base}}/modules/distribution/src/main/config/fluo-conn.properties
[phrasecount]: https://github.com/astralway/phrasecount
[process]: {{ page.docs_base }}/administration/run-fluo-processes
[yarn]: {{ page.docs_base }}/administration/run-fluo-in-yarn
[docker]: {{ page.docs_base }}/administration/run-fluo-in-docker
[manage]: {{ page.docs_base }}/administration/manage-applications
