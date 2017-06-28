---
title: Application Configuration
---

Fluo applications are distributed applications where code is running on many separate machines.
Getting configuration to these distributed processes can be tricky and cumbersome.  Fluo provides
two simple mechanisms to assists with this: application configuration and observer configuration.
This configuration data is stored in ZooKeeper when an application is initialized.  After
initialization any Fluo client or Observer can access the configuration.

## Application Configuration

To use application configuration, set properties with the prefix `fluo.app` in your configuration
file before initialization.  Alternatively use [FluoConfiguration.getAppConfiguration()][fcogac] to
set these properties programmatically.  After Fluo is initialized this information can be accessed
anywhere by calling [FluoClient.getAppConfiguration()][fclgac],
[ObserverProvider.Context.getAppConfigurtaion()][opgac], or [Loader.Context.getAppConfiguration()][lcgac].

The following is a simple example of using application config.   This example sets some application
config before initialization.  After initialization the configuration is accessed via
FluoConfiguration.

```java
  private static void preInit(FluoConfiguration fluoConfig) {
    SimpleConfiguration appConfig = fluoConfig.getAppConfiguration();
    appConfig.setProperty("exporterClass", "com.foo.MysqlExporter");
    appConfig.setProperty("exporterDB", "db1");
    appConfig.setProperty("exporterTable", "table5");
  }

  private static void exercise(MiniFluo mini, FluoClient client) {
    SimpleConfiguration appConfig = client.getAppConfiguration();
    System.out.println(appConfig.getString("exporterClass"));
    System.out.println(appConfig.getString("exporterDB"));
    System.out.println(appConfig.getString("exporterTable"));
  }
```

The code above prints out the following.

```
com.foo.MysqlExporter
db1
table5
```

## Observer Configuration

If you want to use the same code to create multiple observers, one way to accomplish this is
with application configuration. The code below shows an example of this.  The example simulates
exporting rows to multiple mysql tables.  To do this, it creates an observers per a export
table. The observed column and export table for each observer is derived from application
configuration.

```java
  public static class TourObserverProvider implements ObserverProvider {
    @Override
    public void provide(Registry obsRegistry, Context ctx) {
      SimpleConfiguration appCfg = ctx.getAppConfiguration();
      String exportDB = appCfg.getString("exportDB");

      // Create an observer for each export table
      for (Entry<String, String> entry : appCfg.subset("exportTables").toMap().entrySet()) {
        String exportId = entry.getKey();
        String exportTable = entry.getValue();

        Column exportNtfyCol = new Column("ET", exportId);

        Observer exportObserver = (tx, row, col) -> {
          CellScanner scanner = tx.scanner().over(Span.exact(row)).build();

          for (RowColumnValue rcv : scanner) {
            System.out.printf("Exporting val=%s from row=%s to db=%s table=%s\n", rcv.getsValue(),
                row, exportDB, exportTable);
            tx.delete(rcv.getRow(), rcv.getColumn());
          }
        };

        obsRegistry.forColumn(exportNtfyCol, NotificationType.WEAK).useObserver(exportObserver);
      }
    }
  }

  private static void preInit(FluoConfiguration fluoConfig) {
    SimpleConfiguration appConfig = fluoConfig.getAppConfiguration();
    appConfig.setProperty("exportDB", "db1");

    // An observer will be created to process each export table. In this example 't1' and 't2'
    // are used as logical IDs for export tables.
    appConfig.setProperty("exportTables.t1", "bigtable");
    appConfig.setProperty("exportTables.t2", "tinytable");

    fluoConfig.setObserverProvider(TourObserverProvider.class);
  }

  private static void exercise(MiniFluo mini, FluoClient client) {
    try (Transaction tx = client.newTransaction()) {
      tx.set("e:99", new Column("export", "data1"), "222");
      tx.set("e:99", new Column("export", "data2"), "444");
      tx.set("e:99", new Column("export", "data3"), "555");

      tx.setWeakNotification("e:99", new Column("ET", "t1"));

      tx.commit();
    }


    try (Transaction tx = client.newTransaction()) {
      tx.set("e:98", new Column("export", "data1"), "777");
      tx.set("e:98", new Column("export", "data2"), "888");
      tx.set("e:98", new Column("export", "data3"), "999");

      tx.setWeakNotification("e:98", new Column("ET", "t2"));

      tx.commit();
    }

    mini.waitForObservers();
  }
```

Running the code above prints the following.

```
Exporting val=777 from row=e:98 to db=db1 table=tinytable
Exporting val=888 from row=e:98 to db=db1 table=tinytable
Exporting val=999 from row=e:98 to db=db1 table=tinytable
Exporting val=222 from row=e:99 to db=db1 table=bigtable
Exporting val=444 from row=e:99 to db=db1 table=bigtable
Exporting val=555 from row=e:99 to db=db1 table=bigtable
```

[fcogac]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/config/FluoConfiguration.html#getAppConfiguration--
[fclgac]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/FluoClient.html#getAppConfiguration--
[opgac]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/observer/ObserverProvider.Context.html#getAppConfiguration--
[lcgac]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/Loader.Context.html#getAppConfiguration--
[ospec]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release}}/org/apache/fluo/api/config/ObserverSpecification.html
[ocgp]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/observer/Observer.Context.html#getObserverConfiguration--


