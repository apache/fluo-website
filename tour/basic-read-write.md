---
title: Read and Write Data
tour_num: 4
permalink: /tour/4/
---

The following example shows basic code for writing data using Fluo and then
reading it back out.  To run this code modify `src/main/java/ft/Main.java` in
[Fluo Tour git repository][1] and run it following the instructions on the
repository.


```java
  private static void excercise(MiniFluo mini, FluoClient client) {
    String row = "kerbalnaut0001";
    Column fName = new Column("name", "first");
    Column lName = new Column("name", "last");

    try (Transaction tx = client.newTransaction()) {
      tx.set(row, fName, "Jebediah");
      tx.set(row, lName, "Kerman");
      tx.commit();
    }

    try (Snapshot snaphot = client.newSnapshot()) {
      System.out.println("First name : " + snaphot.gets(row, fName));
      System.out.println("Last name  : " + snaphot.gets(row, lName));
    }
  }
```

In the example above a Transaction is created in a try with resources block.  A
Transaction can read and write data.  It can only read data that was committed
before it started.  Data set on a transaction will only be written when
`commit()` is called.
  
A Snapshot is created to read the data previously written by the Transaction.
Snapshots only allow reading data that was commited before the snapshot was
created.  The code calls `gets()` which is a convience method that returns a
Java string.  Internally Fluo only deals with bytes and its `get()` method
returns bytes.   The Fluo methods that take and return Strings assume UTF-8
encoding when converting to bytes.

[1]:https://github.com/keith-turner/fluo-tour
