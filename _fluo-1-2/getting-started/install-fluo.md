---
title: Install Fluo
category: getting-started
order: 3
---

Instructions for installing Apache Fluo and starting a Fluo application on a cluster where
Accumulo, Hadoop & Zookeeper are running.  If you need help setting up these dependencies, see the
[related projects page][related] for external projects that may help.

## Requirements

Before you install Fluo, the following software must be installed and running on your local machine
or cluster:

| Software    | Recommended Version | Minimum Version |
|-------------|---------------------|-----------------|
| [Accumulo]  | 1.8.1               | 1.7.0           |
| [Hadoop]    | 2.7.5               | 2.6.0           |
| [Zookeeper] | 3.4.11              |                 |
| [Java]      | JDK 8               | JDK 8           |

## Obtain a distribution

Before you can install Fluo, you will need to obtain a distribution tarball. It is recommended that
you download the [latest release]. You can also build a distribution from the main branch by following
these steps which create a tarball in `modules/distribution/target`:

    git clone https://github.com/apache/fluo.git
    cd fluo/
    mvn package

## Install Fluo

After you obtain a Fluo distribution tarball, follow these steps to install Fluo.

1.  Choose a directory with plenty of space and untar the distribution:

        tar -xvzf fluo-{{ page.version }}-bin.tar.gz
        cd fluo-{{ page.version }}

    The distribution contains a `fluo` script in `bin/` that administers Fluo and the
    following configuration files in `conf/`:

    | Configuration file           | Description                                                                                  |
    |------------------------------|----------------------------------------------------------------------------------------------|
    | [fluo-env.sh]                | Configures classpath for `fluo` script. Required for all commands.                           |
    | [fluo-conn.properties]       | Configures connection to Fluo. Required for all commands.                                    |
    | [fluo-app.properties]        | Template for configuration file passed to `fluo init` when initializing Fluo application.    |
    | [log4j.properties]           | Configures logging                                                                           |
    | [fluo.properties.deprecated] | Deprecated Fluo configuration file. Replaced by fluo-conn.properties and fluo-app.properties |

2.  Configure [fluo-env.sh] to set up your classpath using jars from the versions of Hadoop, Accumulo, and
Zookeeper that you are using. Choose one of the two ways below to make these jars available to Fluo:

    * Set `HADOOP_PREFIX`, `ACCUMULO_HOME`, and `ZOOKEEPER_HOME` in your environment or configure
    these variables in [fluo-env.sh]. Fluo will look in these locations for jars.
    * Run `./lib/fetch.sh ahz` to download Hadoop, Accumulo, and Zookeeper jars to `lib/ahz` and
    configure [fluo-env.sh] to look in this directory. By default, this command will download the
    default versions set in [lib/ahz/pom.xml]. If you are not using the default versions, you can
    override them:

            ./lib/fetch.sh ahz -Daccumulo.version=1.7.2 -Dhadoop.version=2.7.2 -Dzookeeper.version=3.4.8

3. Fluo needs more dependencies than what is available from Hadoop, Accumulo, and Zookeeper. These
   extra dependencies need to be downloaded to `lib/` using the command below:

        ./lib/fetch.sh extra

You are now ready to use the `fluo` script.

## Fluo command script

The Fluo command script is located at `bin/fluo` of your Fluo installation. All Fluo commands are
invoked by this script.

Modify and add the following to your `~/.bashrc` if you want to be able to execute the fluo script
from any directory:

    export PATH=/path/to/fluo-{{ page.version }}/bin:$PATH

Source your `.bashrc` for the changes to take effect and test the script

    source ~/.bashrc
    fluo

Running the script without any arguments prints a description of all commands.

    ./bin/fluo

## Tuning Accumulo

Fluo will reread the same data frequently when it checks conditions on mutations. When Fluo
initializes a table it enables data caching to make this more efficient. However you may need to
increase the amount of memory available for caching in the tserver by increasing
`tserver.cache.data.size`. Increasing this may require increasing the maximum tserver java heap size
in `accumulo-env.sh`.

Fluo will run many client threads, will want to ensure the tablet server has enough threads. Should
probably increase the `tserver.server.threads.minimum` Accumulo setting.

Using at least Accumulo 1.6.1 is recommended because multiple performance bugs were fixed.

## Next Steps

[Create a Fluo application][create] to run or use [an example application][related].

[Accumulo]: https://accumulo.apache.org/
[Hadoop]: http://hadoop.apache.org/
[Zookeeper]: http://zookeeper.apache.org/
[Java]: http://openjdk.java.net/
[related]: /related-projects/
[latest release]: /release/fluo-{{ site.latest_fluo_release }}/
[fluo-conn.properties]: {{ page.github_base }}/modules/distribution/src/main/config/fluo-conn.properties
[fluo-app.properties]: {{ page.github_base }}/modules/distribution/src/main/config/fluo-app.properties
[log4j.properties]: {{ page.github_base }}/modules/distribution/src/main/config/log4j.properties
[fluo.properties.deprecated]: {{ page.github_base }}/modules/distribution/src/main/config/fluo.properties.deprecated
[fluo-env.sh]: {{ page.github_base }}/modules/distribution/src/main/config/fluo-env.sh
[lib/ahz/pom.xml]: {{ page.github_base }}/modules/distribution/src/main/lib/ahz/pom.xml
[create]: {{ page.docs_base }}/getting-started/create-application
