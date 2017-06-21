---
title: Snapshot Isolation Code
---

```java
  private static void exercise(MiniFluo mini, FluoClient client) {

    String row = "kerbalnaut0001";
    Column lName = new Column("name", "last");

    try(Transaction tx1 = client.newTransaction()) {
      tx1.set(row, lName, "Kerbin");
      tx1.commit();
    }

    try(Transaction tx2 = client.newTransaction()) {
      tx2.set(row, lName, "Kerman");

      Snapshot s1 = client.newSnapshot();

      tx2.commit();

      Snapshot s2 = client.newSnapshot();

      System.out.println(s1.gets(row, lName));
      System.out.println(s2.gets(row, lName));

      s1.close();
      s2.close();
    }
  }
```

The code above prints :

```
Kerbin
Kerman
```


