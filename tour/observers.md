---
title: Observer Concepts
---

Fluo supports incremental processing with Observers and Notifications.  Notifications are persistent
markers set by a transaction that indicate an Observer should run later for a certain row+column.
Observers are user provided code that are registered to process notifications for a certain column. When
an Observer is run, its provided with the row and column that caused it to run along with a
transaction. Fluo worker processes running across a cluster will execute Observers.

Since all transactions need to know which columns trigger Observers, Observers must be registered
with Fluo at initialization time.

Fluo supports two type of notifications :

 * **Strong notifications:** guarantee an observer will run at most once when a column is modified.
   If multiple transactions modify an observed row+column before an observer runs, it will only run
   once.   It will not run once for each modification.
 * **Weak notifications:** cause an observer to run at least once.  Observers may run multiple times
   and/or concurrently based on a single weak notification.  In order to guarantee strong
   notifications run an observer at most once, strong notifications are part of the transaction
   model. Therefore a strong notification can cause transaction collisions.  Weak notifications are
   not transactional and will not cause collisions. Therefore in situations where many transactions
   are notifying a row+column concurrently, using weak notifications is best.


