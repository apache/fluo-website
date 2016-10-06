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
[Observer.Context.getAppConfigurtaion()][ocgac], or [Loader.Context.getAppConfiguration()][lcgac].

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

  private static void excercise(MiniFluo mini, FluoClient client) {
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

If you want instances of an Observer to behave differently and share code, one way to accomplish
this is with per observer configuration.  When setting up an observer call one of the
[ObserverSpecification][ospec] methods that takes configuration.  When an observer is initialized it
can access this configuration by calling [Observer.Context.getObserverConfiguration()][ocgp].

The code below shows an example of setting configuration for an Observer.  This example simulates an
observer that can export rows to a mysql table. The example configures two instances of an observer
using the same class with different configuration.  Even though the observers use the same class, the
two instances must observe different columns.  That is why the code derives the observed column based
on the observer configuration.  Notice the mysql database is obtained from application configuration by
the observer and the table is obtained from observer configuration.

```java
package ft;

import org.apache.fluo.api.client.TransactionBase;
import org.apache.fluo.api.client.scanner.CellScanner;
import org.apache.fluo.api.data.Bytes;
import org.apache.fluo.api.data.Column;
import org.apache.fluo.api.data.RowColumnValue;
import org.apache.fluo.api.data.Span;
import org.apache.fluo.api.observer.Observer;

public class MysqlExportObserver implements Observer {

  private String exportDB;
  private String exportTable;

  @Override
  public void close() {}

  @Override
  public ObservedColumn getObservedColumn() {
    Column col = new Column("ET", exportTable);
    return new ObservedColumn(col, NotificationType.WEAK);
  }

  @Override
  public void init(Context ctx) throws Exception {
    exportDB = ctx.getAppConfiguration().getString("exportDB");
    exportTable = ctx.getObserverConfiguration().getString("exportTable");
  }

  @Override
  public void process(TransactionBase tx, Bytes row, Column col) throws Exception {
    CellScanner scanner = tx.scanner().over(Span.exact(row)).build();

    for (RowColumnValue rcv : scanner) {
      System.out.printf("Exporting val:%s from row:%s to db/table:%s/%s\n", rcv.getsValue(), row,
          exportDB, exportTable);
      tx.delete(rcv.getRow(), rcv.getColumn());
    }
  }
}
```

The following code initializes two observers using the same class with different configuration.  It
also sets application configuration that is used by the observers.  The code then writes some data
and notifies the two observers which process the data.

```java
  private static void preInit(FluoConfiguration fluoConfig) {
    SimpleConfiguration appConfig = fluoConfig.getAppConfiguration();
    appConfig.setProperty("exportDB", "db1");

    ObserverSpecification observer1 = new ObserverSpecification(MysqlExportObserver.class.getName(),
        Collections.singletonMap("exportTable", "table9"));

    ObserverSpecification observer2 = new ObserverSpecification(MysqlExportObserver.class.getName(),
        Collections.singletonMap("exportTable", "table3"));

    fluoConfig.addObserver(observer1);
    fluoConfig.addObserver(observer2);
  }

  private static void excercise(MiniFluo mini, FluoClient client) {
    try (Transaction tx = client.newTransaction()) {
      tx.set("e:99", new Column("export", "data1"), "222");
      tx.set("e:99", new Column("export", "data2"), "444");
      tx.set("e:99", new Column("export", "data3"), "555");

      tx.setWeakNotification("e:99", new Column("ET", "table3"));

      tx.commit();
    }


    try (Transaction tx = client.newTransaction()) {
      tx.set("e:98", new Column("export", "data1"), "777");
      tx.set("e:98", new Column("export", "data2"), "888");
      tx.set("e:98", new Column("export", "data3"), "999");

      tx.setWeakNotification("e:98", new Column("ET", "table9"));

      tx.commit();
    }

    mini.waitForObservers();
  }
```

Running the code above prints the following.

```
Exporting val:222 from row:e:99 to db/table:db1/table3
Exporting val:777 from row:e:98 to db/table:db1/table9
Exporting val:444 from row:e:99 to db/table:db1/table3
Exporting val:888 from row:e:98 to db/table:db1/table9
Exporting val:555 from row:e:99 to db/table:db1/table3
Exporting val:999 from row:e:98 to db/table:db1/table9
```

[fcogac]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/config/FluoConfiguration.html#getAppConfiguration--
[fclgac]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/FluoClient.html#getAppConfiguration--
[ocgac]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/observer/Observer.Context.html#getAppConfiguration--
[lcgac]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/Loader.Context.html#getAppConfiguration--
[ospec]: /apidocs/fluo/{{ site.latest_fluo_release}}/org/apache/fluo/api/config/ObserverSpecification.html
[ocgp]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/observer/Observer.Context.html#getObserverConfiguration--


