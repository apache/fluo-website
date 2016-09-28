---
title: Observer Example
---

The following code shows how to setup and trigger an observer.  The observer is triggered when the
column *obs:data* is changed.

```java
  public static final Column OBSERVED_COL = new Column("obs","data");
  public static final Column INVERT_COL = new Column("inv","data");

  public static class MyObserver extends AbstractObserver {

    @Override
    public void process(TransactionBase tx, Bytes row, Column col) throws Exception {
      //invert column and value
      Bytes value = tx.get(row, col);
      tx.set(value, INVERT_COL, row);
    }

    @Override
    public ObservedColumn getObservedColumn() {
      return new ObservedColumn(OBSERVED_COL, NotificationType.STRONG);
    }
  }

  private static void preInit(FluoConfiguration fluoConfig) {
    //configure Fluo to use MyObserver before initialization
    fluoConfig.addObserver(new ObserverSpecification(MyObserver.class.getName()));
  }

  private static void excercise(MiniFluo mini, FluoClient client) {
    try(Transaction tx1 = client.newTransaction()) {
      tx1.set("kerbalnaut0001", OBSERVED_COL, "Jebediah");
      tx1.commit();
    }

    try(Transaction tx2 = client.newTransaction()) {
      tx2.set("kerbalnaut0002", OBSERVED_COL, "Bill");
      tx2.commit();
    }

    mini.waitForObservers();

    try(Snapshot snap = client.newSnapshot()) {
      snap.scanner().build().forEach(System.out::println);
    }
  }
```

The code above prints :

```
Bill inv data  kerbalnaut0002
Jebediah inv data  kerbalnaut0001
kerbalnaut0001 obs data  Jebediah
kerbalnaut0002 obs data  Bill
```

The following events happen when this code is run.

 * *tx1* modifies *kerbalnaut0001:obs:data* causing *MyObserver* to run later on that row+column.
 * *tx2* modifies *kerbalnaut0002:obs:data* causing *MyObserver* to run later on that row+column.
 * Later *MyObserver* is run and passed row+column *kerbalnaut0001:obs:data*
 * Later *MyObserver* is run and passed row+column *kerbalnaut0002:obs:data*

Observers are run in the background by Fluo threads.  Fluo also creates the
transaction passed to an Observer and commits it.  The transaction does not
need to call commit and can not, the TransactionBase type passed to an Observer
does not have a commit method.   The framework handles committing because it
retries in case of a commit exception.

Since observers are run in the background, you never know when they will run.
For testing purposes MiniFluo provides the waitForObservers() method that is
called above.  This method waits for all notifications to be processed by
observers.

There is no stand alone exercise for the Observer.  Hands on experience with it can be obtained by
completing the [word count exercise](/tour/exercise-1/) which is the next step in the tour.

