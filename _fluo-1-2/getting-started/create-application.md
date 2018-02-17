---
title: Create Application
category: getting-started
order: 4
---

Once you have [Fluo installed][install-fluo], you can create and run Fluo applications consisting
of [clients and observers][design]. This documentation shows how to create a Fluo client and observer.

## Fluo Maven Dependencies

For both clients and observers, you will need to include the following in your Maven pom:

```xml
<dependency>
  <groupId>org.apache.fluo</groupId>
  <artifactId>fluo-api</artifactId>
  <version>{{ page.version }}</version>
</dependency>
<dependency>
  <groupId>org.apache.fluo</groupId>
  <artifactId>fluo-core</artifactId>
  <version>{{ page.version }}</version>
  <scope>runtime</scope>
</dependency>
```

Fluo provides a classpath command to help users build a runtime classpath. This command along with
the `hadoop jar` command is useful when writing scripts to run Fluo client code. These commands
allow the scripts to use the versions of Hadoop, Accumulo, and Zookeeper installed on a cluster.

## Creating a Fluo client

To create a [FluoClient], you will need to provide it with a [FluoConfiguration] object that is
configured to connect to your Fluo instance.

If you have access to the [fluo-conn.properties] file that was used to configure your Fluo instance, you
can use it to build a [FluoConfiguration] object with all necessary properties:

```java
FluoConfiguration config = new FluoConfiguration(new File("fluo-conn.properties"));
config.setApplicationName("myapp");
```

You can also create an empty [FluoConfiguration] object and set properties using Java:

```java
FluoConfiguration config = new FluoConfiguration();
config.setInstanceZookeepers("localhost/fluo");
config.setApplicationName("myapp");
```

Once you have [FluoConfiguration] object, pass it to the `newClient()` method of [FluoFactory] to
create a [FluoClient]:

```java
try(FluoClient client = FluoFactory.newClient(config)){

  try (Transaction tx = client.newTransaction()) {
    // read and write some data
    tx.commit();
  }

  try (Snapshot snapshot = client.newSnapshot()) {
    //read some data
  }
}
```

It may help to reference the [API javadocs][API] while you are learning the Fluo API.

## Creating a Fluo observer

To create an observer, follow these steps:

1.  Create one or more classes that extend [Observer] like the example below. It is a good idea to
    use [slf4j] for any logging in observers as [slf4j] supports multiple logging implementations.

    ```java
    public class InvertObserver implements Observer {

      @Override
      public void process(TransactionBase tx, Bytes row, Column col) throws Exception {
        // read value
        Bytes value = tx.get(row, col);
        // invert row and value
        tx.set(value, new Column("inv", "data"), row);
      }
    }
    ```

2.  Create a class that implements [ObserverProvider] like the example below.  The purpose of this
    class is associate a set Observers with columns that trigger the observers.  The class can
    register multiple observers.

    ```java
    class AppObserverProvider implements ObserverProvider {
      @Override
      public void provide(Registry reg, Context ctx) {
        //setup InvertObserver to be triggered when the column obs:data is modified
        reg.forColumn(new Column("obs", "data"), NotificationType.STRONG)
          .useObserver(new InvertObserver());
        
        //Observer is a Functional interface.  So Observers can be written as lambdas.
        reg.forColumn(new Column("new","data"), NotificationType.WEAK)
          .useObserver((tx,row,col) -> {
             Bytes combined = combineNewAndOld(tx,row);
             tx.set(row, new Column("current","data"), combined);
           });
      }
    }
    ```

3.  Build a jar containing these classes. Put this jar and any other dependencies required for your
    application in a directory. Set `fluo.observer.init.dir` in [fluo-app.properties] to the path of
    this directory. When your application is initialized, these jars will be loaded to HDFS to make
    them accessible to all of your Fluo workers on the cluster.
4.  Configure your Fluo application to use your observer provider by modifying the Application section of
    [fluo-app.properties]. Set `fluo.observer.provider` to the observer provider class name.
5.  Initialize your Fluo application as described in the next section.  During initialization Fluo
    will obtain the observed columns from the ObserverProvider and persist the columns in Zookeeper.
    These columns persisted in Zookeeper are used by transactions to know when to trigger observers.

## Next Steps

[Initialize] your Fluo application before running it.

[design]: {{ page.docs_base }}/getting-started/design
[install-fluo]: {{ page.docs_base }}/getting-started/install-fluo
[Initialize]: {{ page.docs_base }}/administration/initialize
[FluoFactory]: {{ page.javadoc_base}}/org/apache/fluo/api/client/FluoFactory.html
[FluoClient]: {{ page.javadoc_base}}/org/apache/fluo/api/client/FluoClient.html
[FluoConfiguration]: {{ page.javadoc_base}}/org/apache/fluo/api/config/FluoConfiguration.html
[Observer]: {{ page.javadoc_base}}/org/apache/fluo/api/observer/Observer.html
[ObserverProvider]: {{ page.javadoc_base}}/org/apache/fluo/api/observer/ObserverProvider.html
[fluo-conn.properties]: {{ page.github_base}}/modules/distribution/src/main/config/fluo-conn.properties
[fluo-app.properties]: {{ page.github_base}}/modules/distribution/src/main/config/fluo-app.properties
[API]: https://fluo.apache.org/apidocs/
[slf4j]: http://www.slf4j.org/
[logback]: http://logback.qos.ch/
