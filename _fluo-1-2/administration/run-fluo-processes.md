---
title: Run Fluo processes
category: administration
order: 2
---

An Apache Fluo application consists of an oracle process and multiple worker processes.  These processes
can be manually started by users on a single node or distributed across a cluster.

## Requirements

Each node where Fluo is run must have [Fluo installed][install-fluo].

## Start Fluo processes

Follow the instructions below to start Fluo processes.

1. Configure [fluo-env.sh] and [fluo-conn.properties] if you have not already.

2. Run Fluo application processes using the `fluo oracle` and `fluo worker` commands. Fluo applications
   are typically run with one oracle process and multiple worker processes. The commands below will start
   a Fluo oracle and two workers on your local machine:

        fluo oracle -a myapp &> oracle.log &
        fluo worker -a myapp &> worker1.log &
        fluo worker -a myapp &> worker2.log &

   The commands will retrieve your application configuration and observer jars (using your
   application name) before starting the oracle or worker process.

If you want to distribute the processes of your Fluo application across a cluster, you will need install
Fluo on every node where you want to run a Fluo process. It is recommended that you use a cluster management
tool like Salt, Ansible, or Chef to install and run Fluo on a cluster.

## Stop Fluo processes

To stop your Fluo application, run `jps -m | grep Fluo` to find process IDs and use `kill` to stop them.

## Next Steps

Learn how to [manage Fluo applications][manage].

[install-fluo]: {{ page.docs_base }}/getting-started/install-fluo
[manage]: {{ page.docs_base }}/administration/manage-applications
[fluo-env.sh]: {{ page.github_base}}/modules/distribution/src/main/config/fluo-env.sh
[fluo-conn.properties]: {{ page.github_base}}/modules/distribution/src/main/config/fluo-conn.properties
