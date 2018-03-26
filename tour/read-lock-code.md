---
title: Read Lock Code
---

```java
  private static final Column WEIGHT_COL = new Column("stat", "weight");

  private static void exercise(MiniFluo mini, FluoClient client) {
    try (Transaction tx1 = client.newTransaction()) {
      tx1.set("kerbalnaut0001", WEIGHT_COL, "90");
      tx1.set("kerbalnaut0002", WEIGHT_COL, "70");
      tx1.set("kerbalnaut0003", WEIGHT_COL, "80");
      tx1.commit();
    }

    try (Transaction tx2 = client.newTransaction();
         Transaction tx3 = client.newTransaction();
         Transaction tx4 = client.newTransaction())
    {
      int f1w1 = Integer.parseInt(tx2.withReadLock().gets("kerbalnaut0001", WEIGHT_COL));
      int f1w2 = Integer.parseInt(tx2.withReadLock().gets("kerbalnaut0003", WEIGHT_COL));
      tx2.set("flight0001", WEIGHT_COL, f1w1 + f1w2 + "");

      int f2w1 = Integer.parseInt(tx3.withReadLock().gets("kerbalnaut0001", WEIGHT_COL));
      int f2w2 = Integer.parseInt(tx3.withReadLock().gets("kerbalnaut0002", WEIGHT_COL));
      tx3.set("flight0002", WEIGHT_COL, f2w1 + f2w2 + "");

      tx4.set("kerbalnaut0001", WEIGHT_COL, "95");

      for(Transaction ctx : Arrays.asList(tx2,tx3,tx4)) {
        try {
         ctx.commit();
        } catch (CommitException ce) {
          System.out.println("commit failed: "+ce.getMessage());
        }
      }
    }

    try(Snapshot snap = client.newSnapshot()) {
      snap.scanner().build().forEach(System.out::println);
    }
  }
```

Output :

```
commit failed: Collisions(1):kerbalnaut0001 stat weight
flight0001 stat weight  170
flight0002 stat weight  160
kerbalnaut0001 stat weight  90
kerbalnaut0002 stat weight  70
kerbalnaut0003 stat weight  80
```

Output for commit order `Arrays.asList(tx4,tx2,tx3)` :

```
commit failed: Collisions(1):kerbalnaut0001 stat weight
commit failed: Collisions(1):kerbalnaut0001 stat weight
kerbalnaut0001 stat weight  95
kerbalnaut0002 stat weight  70
kerbalnaut0003 stat weight  80
```

With this commit order *tx4* gets a write lock on *kerbalnaut0001:stat:weight*
which prevents *tx2* and *tx3* from getting read locks.
