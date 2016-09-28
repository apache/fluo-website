---
title: Observer Concepts
---

Fluo supports complex processing by running user provided Observers which are triggered by
notifications.   An Observer request that the system run it when a certain column is modified.  When
another transaction modifies an observed column, it will persist a notification that later causes
the Observer to run.  When an Observers is run, its provided with the row and column that caused it
to run along with a transaction.  Fluo worker processes running across a cluster will execute
Observers.

Since all transactions need to know which columns trigger observers, observer must be registered
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


