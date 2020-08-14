---
title: "Loading data into Fluo using Apache Spark"
date: 2016-12-22 11:43:00 +0000
author: Keith Turner
reviewers: Mike Walch
---

[Apache Spark][spark] can be used to preprocess and load batches of data into Fluo.  For example
Spark could be used to group data within a batch and then Fluo transactions could load groups of
related data. This blog post offers some tips to help you get started writing to Fluo from Spark.

### Executing load transactions in Spark

Spark automatically serializes Java objects that are needed for remote execution.  When trying to
use Fluo with Spark its important to understand what will serialize properly and what will not.
Classes used to load data into Fluo like [FluoClient] and [LoaderExecutor] are not suitable for
serialization.  These classes may have thread pools, resources in Zookeeper, transactions that are
committing in the background, etc .  Therefore these classes must be instantiated at each remote process
Spark creates.  One way to do this is with Spark's `foreachParition` method.  This method will
execute code locally at each RDD partition. Within each partition, a [LoaderExecutor]
can be created.  That's what the example below shows. 

```java
 
public void dedupeAndLoad(JavaRDD<Document> docRdd, int numPartitions) {  

  // Remove duplicate documents.
  docRdd = docRdd.distinct(numPartitions);
  
  // Execute load transactions for unique documents.  Iin Java 8 lambda syntax below, 
  // iter is of type Iterator<Document>
  docRdd.foreachPartition(iter->{
    // Assume fluo.properties file was submitted with application
    FluoConfiguration fconf = new FluoConfiguration(new File("fluo.properties"));
    try(FluoClient client = FluoFactory.newClient(fconf); 
        LoaderExecutor le = client.newLoaderExecutor())
    {
      while(iter.hasNext()) {
        le.execute(new DocumentLoader(iter.next()));
      }
    }
  });
}
```

The example above requires that `fluo.properties` is available locally for each
partition.  This can be accomplished with `--files` option when launching a Spark job.

```
spark-submit --class myApp.Load --files <fluo props dir>/fluo.properties myApp.jar
```

If FluoConfiguration were serializable, then Spark could automatically serialize and make a
FluoConfiguration object available for each partition.  However, FluoConfiguration is not
serializable as of Fluo 1.0.0.  This will be fixed in future releases of Fluo.  See [#813][fluo-813]
for details and workarounds for 1.0.0.

### Initializing Fluo table

If you have a lot of existing data, then you could use Spark to initialize your Fluo table with
historical data. There are two general ways to do this.  The simplest way is to use the
[AccumuloOutputFormat] to write [Mutation] objects to Accumulo.  However, you need to write data
using the Fluo data format.  Fluo provides an easy way to do this using the [FluoMutationGenerator].  

A slightly more complex way to initialize a Fluo table is using Accumulo's bulk load mechanism.
Bulk load is the process of generating Accumulo RFile's containing Key/Values in a Spark job. Those
files are then loaded into an Accumulo table.   This can be faster, but its more complex because it
requires the user to properly partition data in their Spark job.  Ideally, these partitions would
consist of non-overlapping ranges of Accumulo keys with roughly even amounts of data.  The default
partitioning methods in Spark will not accomplish this.    

When following the bulk load approach, you would write [Key] and [Value] objects using the
[AccumuloFileOutputFormat]. Fluo provides the [FluoKeyValueGenerator] to create key/values in the
Fluo data format.  Fluo Recipes builds on this and provides code that makes it easy to bulk import
into Accumulo.  The [FluoSparkHelper.bulkImportRcvToFluo()][bi2fluo] method will do the following :

 * Repartition data using the split points in the Fluo table
 * Convert data into expected format for a Fluo table
 * Create an RFile for each partition in a specified temp dir
 * Bulk import the RFiles into the Fluo table

The [Webindex] example uses bulk load to initialize its Fluo table using the code in Fluo Recipes.
Webindex uses multiple [Collision Free Maps][cfm] and initializes them using
[CollisionFreeMap.getInitializer()][cfminit].  Webindex uses Spark to initialize the Fluo table with
historical data.  Webindex also uses Spark to execute load transactions in parallel for
incrementally loading data. 

### Packaging your code to run in Spark

One simple way to execute your Spark code is to create a shaded jar.  This shaded jar should contain
\: Accumulo client code, Fluo client code, Zookeeper client code, and your Application code.  It
would be best if the shaded jar contained the versions of Accumulo, Fluo, and Zookeeper running on
the target system.  One way to achieve this goal is to make it easy for users of your Fluo
application to build the shaded jar themselves.  The examples below shows a simple bash script and
Maven pom file that achieve this goal.

There is no need to include Spark code in the shaded jar as this will be provided by the Spark
runtime environment.   Depending on your Spark environment, Hadoop client code may also be provided.
Therefore, Hadoop may not need to be included in the shaded jar. One way to exclude these from the
shaded jars is to make the scope of these dependencies `provided`, which is what the example does.
You may also want to consider excluding other libraries that are provided in the Spark env like
Guava, log4j, etc.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.foo</groupId>
  <artifactId>fluoAppShaded</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <packaging>jar</packaging>

  <name>Shaded Fluo App</name>

  <properties>
    <accumulo.version>1.7.2</accumulo.version>
    <fluo.version>1.0.0-incubating</fluo.version>
    <zookeeper.version>3.4.9</zookeeper.version>
  </properties>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-shade-plugin</artifactId>
        <executions>
          <execution>
            <goals>
              <goal>shade</goal>
            </goals>
            <phase>package</phase>
            <configuration>
              <shadedArtifactAttached>true</shadedArtifactAttached>
              <shadedClassifierName>shaded</shadedClassifierName>
              <filters>
                <filter>
                  <artifact>*:*</artifact>
                  <excludes>
                    <exclude>META-INF/*.SF</exclude>
                    <exclude>META-INF/*.DSA</exclude>
                    <exclude>META-INF/*.RSA</exclude>
                  </excludes>
                </filter>
              </filters>
            </configuration>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>

  <!--
       The provided scope is used for dependencies that should not end up in
       the shaded jar.  The shaded jar is used to run Spark jobs. The Spark 
       launcher will provided Spark and Hadoop dependencies, so they are not
       needed in the shaded jar.
  -->

  <dependencies>
    <!-- The dependency on your Fluo application code.  Version of your app could be made configurable. -->
    <dependency>
      <groupId>com.foo</groupId>
      <artifactId>fluoApp</artifactId>
      <version>1.2.3</version>
    </dependency>
    <dependency>
      <groupId>org.apache.fluo</groupId>
      <artifactId>fluo-api</artifactId>
      <version>${fluo.version}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.fluo</groupId>
      <artifactId>fluo-core</artifactId>
      <version>${fluo.version}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.accumulo</groupId>
      <artifactId>accumulo-core</artifactId>
      <version>${accumulo.version}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.zookeeper</groupId>
      <artifactId>zookeeper</artifactId>
      <version>${zookeeper.version}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.hadoop</groupId>
      <artifactId>hadoop-client</artifactId>
      <version>2.7.2</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>org.apache.spark</groupId>
      <artifactId>spark-core_2.10</artifactId>
      <version>1.6.2</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
</project>
```

The following bash script can use the pom above to build a shaded jar.

```bash
# Get the versions of Accumulo and Fluo running on the system.  Could let the
# user of your Fluo application configure this and have this script read that
# config.
ACCUMULO_VERSION=`accumulo version`
FLUO_VERSION=`fluo version`

# Could not find an easy way to get zookeeper version automatically
ZOOKEEPER_SERVER=localhost
ZOOKEEPER_VERSION=`echo status | nc $ZOOKEEPER_SERVER 2181 | grep version: | sed 's/.*version: \([0-9.]*\).*/\1/'`

# Build the shaded jar
mvn package -Daccumulo.version=$ACCUMULO_VERSION \
            -Dfluo.version=$FLUO_VERSION \
            -Dzookeeper.version=$ZOOKEEPER_VERSION
```

There are other possible ways to package and run your Fluo application for Spark.  This section
suggested one possible way.  The core concept of this method is late binding of the Accumulo, Fluo,
Hadoop, Spark, and Zookeeper libraries.  When choosing a method to create a shaded jar, the
implications of early vs late binding is something to consider.

[FluoClient]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/FluoClient.html
[LoaderExecutor]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/LoaderExecutor.html
[bi2fluo]:{{ site.fluo_recipes_spark_static }}/{{ site.latest_recipes_release }}/org/apache/fluo/recipes/spark/FluoSparkHelper.html#bulkImportRcvToFluo-org.apache.spark.api.java.JavaPairRDD-org.apache.fluo.recipes.spark.FluoSparkHelper.BulkImportOptions-
[cfminit]:{{ site.fluo_recipes_core_static }}/{{ site.latest_recipes_release }}/org/apache/fluo/recipes/core/map/CollisionFreeMap.html#getInitializer-java.lang.String-int-org.apache.fluo.recipes.core.serialization.SimpleSerializer-
[cfm]: /docs/fluo-recipes/1.0.0-incubating/cfm/
[fluo-813]: https://github.com/apache/incubator-fluo/issues/813
[AccumuloOutputFormat]: http://accumulo.apache.org/1.8/apidocs/org/apache/accumulo/core/client/mapred/AccumuloOutputFormat.html
[Mutation]: http://accumulo.apache.org/1.8/apidocs/org/apache/accumulo/core/data/Mutation.html
[Key]: http://accumulo.apache.org/1.8/apidocs/org/apache/accumulo/core/data/Key.html
[Value]: http://accumulo.apache.org/1.8/apidocs/org/apache/accumulo/core/data/Value.html
[FluoMutationGenerator]: https://github.com/apache/incubator-fluo/blob/rel/fluo-1.0.0-incubating/modules/mapreduce/src/main/java/org/apache/fluo/mapreduce/FluoMutationGenerator.java
[FluoKeyValueGenerator]: https://github.com/apache/incubator-fluo/blob/rel/fluo-1.0.0-incubating/modules/mapreduce/src/main/java/org/apache/fluo/mapreduce/FluoKeyValueGenerator.java
[AccumuloFileOutputFormat]: http://accumulo.apache.org/1.8/apidocs/org/apache/accumulo/core/client/mapred/AccumuloFileOutputFormat.html
[bulk_readme]: http://accumulo.apache.org/1.8/examples/bulkIngest
[bulk_code]: https://github.com/apache/accumulo/tree/rel/1.8.0/examples/simple/src/main/java/org/apache/accumulo/examples/simple/mapreduce/bulk
[AccumuloRangePartitioner]: https://github.com/apache/incubator-fluo-recipes/blob/rel/fluo-recipes-1.0.0-incubating/modules/spark/src/main/java/org/apache/fluo/recipes/spark/AccumuloRangePartitioner.java
[Webindex]: https://github.com/apache/fluo-examples/tree/main/webindex
[spark]: https://spark.apache.org
