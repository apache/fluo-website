---
title: Write Skew Code
---

```java
 private static void excercise(MiniFluo mini, FluoClient client) {

    Column sumCol = new Column("data", "sum");

    try(Transaction tx1 = client.newTransaction()) {
      tx1.set("n0", sumCol, "0");
      tx1.set("n01", sumCol, "1");
      tx1.set("n02", sumCol, "2");
      tx1.commit();
    }

    try(Transaction tx2 = client.newTransaction(); Transaction tx3 = client.newTransaction()) {

      int n01Sum = Integer.parseInt(tx2.gets("n01", sumCol));
      int n02Sum = Integer.parseInt(tx2.gets("n02", sumCol));

      tx2.set("n0", sumCol, n01Sum + n02Sum +"");
      tx3.set("n01", sumCol, "5");

      tx2.commit();
      tx3.commit();
    }

    try(Snapshot s1 = client.newSnapshot()) {
      System.out.println("n0 sum : "+s1.gets("n0", sumCol));
      System.out.println("n01 sum : "+s1.gets("n01", sumCol));
      System.out.println("n02 sum : "+s1.gets("n02", sumCol));
    }
  }
```

The code above prints :

```
n0  sum : 3
n01 sum : 5
n02 sum : 2
```

