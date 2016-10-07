---
title: Fetching multiple cells
---

Each call to get a row column results in a RPC to an Accumulo server.  In the cases where there are
many row columns to get, Fluo provides more specialized get methods that make less RPC calls.

Below is some example code that illustrates using these methods and shows the performance
difference.  The example code performs the following task.

 * In a single transaction, generates 100 rows each with 100 columns such that each row has the same
   columns.  Uses integers for the row and columns names.
 * Gets 100 columns from a single row in the following ways.  Times each way.
   * In a loop calls  [gets(CharSequence, Column)][get].
   * Calls [gets(CharSequence, Set\<Column\>)][getsc] once
 * Gets 100 columns from 3 rows in the following ways.  Times each way. 
   * For three rows, loops over 100 columns calling  [gets(CharSequence, Column)][get]
   * Calls [gets(Collection\<? extends CharSequence\>, Set\<Column\>)][getmc] once
 * Generates 100 row column pairs, where each pair is a random row and a random column. Gets each
 * pair in the following ways.  Times each way.  
   * For each pair calls [gets(CharSequence, Column)][get]
   * Calls [gets(Collection\<RowColumn\>)][getrc] once

Below is the code to perform the task mentioned above.

```java
  private static void excercise(MiniFluo mini, FluoClient client) {

    Set<Column> columns = new LinkedHashSet<>();

    for(int c = 0; c < 100; c++) {
      columns.add(new Column("f", String.format("q%04d", c)));
    }

    try(Transaction tx = client.newTransaction()) {
      int value = 0;
      for(int r = 0; r < 100; r++) {
        String row = String.format("r%04d", r);
        for (Column column : columns) {
          tx.set(row, column, value+"");
          value++;
        }
      }

      tx.commit();
    }

    //fetch multiple columns from a single row
    try(Snapshot snap = client.newSnapshot()) {
      String row = String.format("r%04d", 42);

      long t1 = System.currentTimeMillis();

      for (Column column : columns) {
        snap.gets(row, column);
      }

      long t2 = System.currentTimeMillis();

      snap.gets(row, columns);

      long t3 = System.currentTimeMillis();

      System.out.printf("test1 time 1:%d  time2:%d\n",(t2-t1),(t3-t2));
    }


    //fetch the same columns from multiple rows
    try(Snapshot snap = client.newSnapshot()) {
      List<String> rows = Arrays.asList(String.format("r%04d", 42),
                                        String.format("r%04d", 21),
                                        String.format("r%04d", 84));

      long t1 = System.currentTimeMillis();

      for (String row : rows) {
        for (Column column : columns) {
          snap.gets(row, column);
        }
      }

      long t2 = System.currentTimeMillis();

      snap.gets(rows, columns);

      long t3 = System.currentTimeMillis();

      System.out.printf("test2 time 1:%d  time2:%d\n",(t2-t1),(t3-t2));
    }

    //fetch different columns from different rows
    try(Snapshot snap = client.newSnapshot()) {
      Random rand = new Random();
      //generate the row columns to fetch
      List<RowColumn> rowcols = new ArrayList<>();
      for(int i = 0; i < 100; i++) {
        String row = String.format("r%04d", rand.nextInt(100));
        Column col = new Column("f", String.format("q%04d", rand.nextInt(100)));
        rowcols.add(new RowColumn(row, col));
      }

      long t1 = System.currentTimeMillis();

      for (RowColumn rowColumn : rowcols) {
        snap.get(rowColumn.getRow(), rowColumn.getColumn());
      }

      long t2 = System.currentTimeMillis();

      snap.gets(rowcols);

      long t3 = System.currentTimeMillis();

      System.out.printf("test3 time 1:%d  time2:%d\n",(t2-t1),(t3-t2));
    }
  }
```

The program above outputs :

```
test1 time 1:294  time2:13
test2 time 1:651  time2:25
test3 time 1:153  time2:7
```

[get]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/SnapshotBase.html#gets-java.lang.CharSequence-org.apache.fluo.api.data.Column-
[getsc]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/SnapshotBase.html#gets-java.lang.CharSequence-java.util.Set-
[getmc]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/SnapshotBase.html#gets-java.util.Collection-java.util.Set-
[getrc]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/SnapshotBase.html#gets-java.util.Collection-

