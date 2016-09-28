---
title: Memory limits and self notify code
---

```java
  static Column NC = new Column("ntyf", "sum");
  static Column TOTAL_COL = new Column("sum", "total");
  static Column UPDATE_COL = new Column("sum", "update");
  static Column CONTINUE_COL = new Column("sum", "continue");

  public static class SummingObserver extends AbstractObserver {

    private int maxToProcess;

    @Override
    public void init(Context context) throws Exception {
      //made the max amount to process in a single transaction configurable
      maxToProcess = context.getObserverConfiguration().getInt("maxToProcess", 100);
    }

    @Override
    public ObservedColumn getObservedColumn() {
      return new ObservedColumn(NC, NotificationType.WEAK);
    }

    @Override
    public void process(TransactionBase tx, Bytes brow, Column col) throws Exception {

      String row = brow.toString();

      Map<Column, String> colVals = tx.gets(row, TOTAL_COL, CONTINUE_COL);

      int sum = Integer.parseInt(colVals.getOrDefault(TOTAL_COL, "0"));
      
      // construct a scan range that uses the continue row
      String startRow = colVals.getOrDefault(CONTINUE_COL, row + "/");
      String endRow = row + "/:"; // after the character '9' comes ':'
      CellScanner scanner = tx.scanner().over(new Span(startRow, true, endRow, false)).build();

      int processed = 0;
      
      for (RowColumnValue rcv : scanner) {
        if (processed >= maxToProcess) {
          // stop processing and set the continue row
          tx.set(row, CONTINUE_COL, rcv.getsRow());
          tx.setWeakNotification(brow, col);
          break;
        }
        sum += Integer.parseInt(rcv.getsValue());
        tx.delete(rcv.getRow(), rcv.getColumn());
        processed++;
      }

      System.out.println("sum : " + sum + "  start: " + startRow + "  processed: " + processed);

      tx.set(row, TOTAL_COL, "" + sum);

      // if did not set the continue column and it exists, then delete it
      if (processed < maxToProcess && colVals.containsKey(CONTINUE_COL)) {
        tx.delete(row, CONTINUE_COL);
        // need to start over at the beginning and see if there is new data before the continue
        // column
        tx.setWeakNotification(brow, col);
      }
    }
  }

  private static void preInit(FluoConfiguration fluoConfig) {
    ObserverSpecification ospec = new ObserverSpecification(SummingObserver.class.getName());
    ospec.getConfiguration().setProperty("maxToProcess", 500);
    fluoConfig.addObserver(ospec);
  }

  private static void excercise(MiniFluo mini, FluoClient client) {
    try (LoaderExecutor le = client.newLoaderExecutor()) {
      Random r = new Random(42);
      for (int i = 0; i < 5000; i++) {
        // The Loader interface only has one function and can therefore be written as a lambda
        // below.
        le.execute((tx, ctx) -> {
          String row = "counter001/" + String.format("%07d", r.nextInt(10000000));
          int curVal = Integer.parseInt(tx.gets(row, UPDATE_COL, "0"));
          tx.set(row, UPDATE_COL, curVal + 1 + "");
          tx.setWeakNotification("counter001", NC);
        });
      }
    }

    mini.waitForObservers();

    try (Snapshot snap = client.newSnapshot()) {
      System.out.println("final sum : " + snap.gets("counter001", TOTAL_COL));
    }
  }
```

The code above will print something like the following.

```
$ mvn -q clean compile exec:java
Starting MiniFluo ... started.
sum : 500  start: counter001/  processed: 500
sum : 891  start: counter001/7945963  processed: 390
sum : 1391  start: counter001/  processed: 500
sum : 1891  start: counter001/2938489  processed: 500
sum : 2391  start: counter001/5210523  processed: 500
sum : 2892  start: counter001/6912090  processed: 500
sum : 3392  start: counter001/8410312  processed: 500
sum : 3398  start: counter001/9991522  processed: 6
sum : 3898  start: counter001/  processed: 500
sum : 4398  start: counter001/1824962  processed: 500
sum : 4899  start: counter001/4076664  processed: 500
sum : 5000  start: counter001/6993690  processed: 101
sum : 5000  start: counter001/  processed: 0
final sum : 5000
```

