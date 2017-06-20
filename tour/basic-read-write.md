---
title: Read and Write Data
---

The following example shows basic code for writing data using Fluo and then reading it back out.  To
run this code, modify `src/main/java/ft/Main.java` in the [Fluo Tour git repository][1] and run it by
following the instructions in the repository.


```java
  private static void exercises(MiniFluo mini, FluoClient client) {
    String row = "kerbalnaut0001";
    Column fName = new Column("name", "first");
    Column lName = new Column("name", "last");

    try (Transaction tx = client.newTransaction()) {
      tx.set(row, fName, "Jebediah");
      tx.set(row, lName, "Kerman");
      tx.commit();
    }

    try (Snapshot snapshot = client.newSnapshot()) {
      System.out.println("First name : " + snapshot.gets(row, fName));
      System.out.println("Last name  : " + snapshot.gets(row, lName));
    }
  }
```

In the example above, a **Transaction** is created in a try-with-resources block.  A Transaction can read
and write data.  It can only read data that was committed before it started.  Data set on a
transaction will only be written when `commit()` is called.

A **Snapshot** is created to read the data previously written by the Transaction.  Snapshots only see
data committed before the snapshot was created.  The code calls [gets(CharSequence, Column)][gets] which
is a convenience method that works with strings.  Internally Fluo only deals with bytes and its
[get(Bytes, Column)][get] method returns [Bytes].   The Fluo methods that take and return Strings
assume UTF-8 encoding when converting to bytes.

Transactions and snapshots allocate resources and therefore have `close()` methods.  The
try-with-resources block will automatically call `close()`, even when exceptions occur.

[1]: https://github.com/apache/incubator-fluo-website/tree/fluo-tour
[get]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/SnapshotBase.html#get-org.apache.fluo.api.data.Bytes-org.apache.fluo.api.data.Column-
[gets]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/SnapshotBase.html#gets-java.lang.CharSequence-org.apache.fluo.api.data.Column-
[Bytes]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/data/Bytes.html
