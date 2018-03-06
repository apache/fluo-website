---
title: Run Fluo in YARN
category: administration
order: 3
---

An Apache Fluo application can be started in Hadoop YARN using the Fluo YARN launcher.

## Requirements

To launch a Fluo application in [YARN], you'll need the following software installed.

| Software             | Recommended Version | Minimum Version |
|----------------------|---------------------|-----------------|
| [Fluo][archive]      | 1.2.0               | 1.2.0           |
| [Fluo YARN][archive] | 1.0.0               | 1.0.0           |
| [YARN]               | 2.7.2               | 2.6.0           |

Instructions for installing Fluo YARN can be found below. See the [related projects page][related] for external projects
that may help in setting up all of these dependencies.

## Set up your Fluo application

Before you can launch a Fluo application in YARN, you should [install Fluo][install] and [initialize your
application][initialize]. After your application has been initialized, follow the instructions below to install
the Fluo YARN launcher and run your application in YARN. Avoid using the `fluo` command to start local oracle
and worker processes if you are running in YARN.

## Install and Configure Fluo YARN launcher

To install the Fluo YARN launcher, you will need to obtain a distribution tarball. It is recommended that you
download the [latest release] but all releases can be found in the [archive]. You can also build a distribution from the
master branch by following these steps which create a tarball in `distribution/target`:

    git clone https://github.com/apache/fluo-yarn.git
    cd fluo-yarn/
    mvn package

After you obtain a Fluo YARN distribution tarball, follow these steps to install Fluo.

1. Choose a directory with plenty of space, untar the distribution, and run `fetch.sh` to retrieve dependencies:

        tar -xvzf fluo-yarn-1.0.0-bin.tar.gz
        cd fluo-yarn-1.0.0
        ./lib/fetch.sh

    The distribution contains a `fluo-yarn` script in `bin/` that administers Fluo and the
    following configuration files in `conf/`:

    | Configuration file          | Description                                                             |
    |-----------------------------|-------------------------------------------------------------------------|
    | [fluo-yarn-env.sh]          | Configures classpath for `fluo-yarn` script. Required for all commands. |
    | [fluo-yarn.properties]      | Configures how application runs in YARN.  Required for `start` command. |
    | [log4j.properties]          | Configures logging                                                      |

2. Configure [fluo-yarn-env.sh]

    * Set `FLUO_HOME` if it is not in your environment
    * Modify `FLUO_CONN_PROPS` if you don't want use the default.

3. Configure [fluo-yarn.properties] to set how your application will be launched in YARN:

    * YARN resource manager hostname
    * Number of oracle and worker instances
    * Max memory usage per oracle/worker

   If you are managing multiple Fluo applications in YARN, you can copy this file and configure it for
   each application.

## Start Fluo application in YARN

Follow the instructions below to start your application in YARN. If you have not done so already, you should [initialize
your Fluo application][initialize] before following these instructions.

1. Configure [fluo-yarn-env.sh] and [fluo-yarn.properties] if you have not already.

2. Run the commands below to start your Fluo application in YARN.

        fluo-yarn start myapp conf/fluo-yarn.properties

   The commands will retrieve your application configuration and observer jars (using your application name) before
   starting the application in YARN. The command will output a YARN application ID that can be used to find your
   application in the YARN resource manager and view its logs.

## Manage Fluo application in YARN

Except for stopping your application in YARN, the `fluo` script can be used to [manage your application][manage] using the
`scan` and `wait` commands.

When you want you stop your Fluo application, use the the YARN resource manager or the 
`yarn application -kill <App ID>` to stop the application in YARN.

[Fluo]: https://fluo.apache.org/
[YARN]: https://hadoop.apache.org/
[related]: /related-projects/
[install]: {{ page.docs_base }}/getting-started/install-fluo
[application]: {{ page.docs_base }}/getting-started/create-application
[initialize]: {{ page.docs_base }}/administration/initialize
[manage]: {{ page.docs_base }}/administration/manage-applications
[latest release]: /release/fluo-yarn-{{ site.latest_fluo_yarn_release }}/
[archive]: /release/
[fluo-yarn-env.sh]: {{ page.github_yarn}}/distribution/conf/fluo-yarn-env.sh
[fluo-yarn.properties]: {{ page.github_yarn}}/distribution/conf/fluo-yarn.properties
[log4j.properties]: {{ page.github_yarn}}/distribution/conf/log4j.properties
