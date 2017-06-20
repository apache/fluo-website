---
title: Weak Notification Code
---

```java
  static Column NC = new Column("ntyf", "sum");
  static Column TOTAL_COL = new Column("sum", "total");
  static Column UPDATE_COL = new Column("sum", "update");

  public static class SummingObserver extends AbstractObserver {

    @Override
    public ObservedColumn getObservedColumn() {
      return new ObservedColumn(NC, NotificationType.WEAK);
    }

    @Override
    public void process(TransactionBase tx, Bytes brow, Column col) throws Exception {

      String row = brow.toString();

      int sum = Integer.parseInt(tx.gets(row, TOTAL_COL, "0"));

      CellScanner scanner = tx.scanner().over(Span.prefix(row +"/")).build();
      for (RowColumnValue rcv : scanner) {
        sum += Integer.parseInt(rcv.getsValue());
        tx.delete(rcv.getRow(), rcv.getColumn());
      }

      System.out.println("sum : " + sum);

      tx.set(row, TOTAL_COL, ""+sum);
    }
  }

  private static void preInit(FluoConfiguration fluoConfig) {
    fluoConfig.addObserver(new ObserverSpecification(SummingObserver.class.getName()));
  }

  private static void exercise(MiniFluo mini, FluoClient client) {
    try (LoaderExecutor le = client.newLoaderExecutor()) {
      Random r = new Random(42);
      for (int i = 0; i < 5000; i++) {
        //The Loader interface only has one function and can therefore be written as a lambda below.
        le.execute((tx, ctx) -> {
          String row = "counter001/"+String.format("%07d", r.nextInt(10_000_000));
          int curVal = Integer.parseInt(tx.gets(row, UPDATE_COL, "0"));
          tx.set(row, UPDATE_COL, curVal+1+"");
          tx.setWeakNotification("counter001", NC);
        });
      }
    }

    mini.waitForObservers();

    try(Snapshot snap = client.newSnapshot()) {
      System.out.println("final sum : "+snap.gets("counter001", TOTAL_COL));
    }
  }
```

The code above will print something like the following.  Every run will print something slightly
different because it depends on when the observer runs.

```
$ mvn -q clean compile exec:java
Starting MiniFluo ... started.
sum : 526
sum : 1465
sum : 2414
sum : 3260
sum : 4736
sum : 5000
final sum : 5000
```
