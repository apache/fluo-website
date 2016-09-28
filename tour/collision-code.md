---
title: Collision code
---

```java
  private static void excercise(MiniFluo mini, FluoClient client) {

    String row = "kerbalnaut0001";
    Column lName = new Column("name", "last");

    try(Transaction tx1 = client.newTransaction()) {
      tx1.set(row, lName, "Kerma");
      tx1.commit();
    }

    try(Transaction tx2 = client.newTransaction(); Transaction tx3 = client.newTransaction()) {

      tx2.set(row, lName, tx2.gets(row, lName)+"n");
      tx3.set(row, lName, tx3.gets(row, lName)+"N");

      tx2.commit();
      try{
        tx3.commit();
      } catch (Exception e) {
        System.out.println("tx3 commit exception : " +e);
      }
    }

    try(Snapshot s1 = client.newSnapshot()) {
      System.out.println(s1.gets(row, lName));
    }
  }
```

The code above prints :

```
tx3 commit exception message : org.apache.fluo.api.exceptions.CommitException
Kerman
```

