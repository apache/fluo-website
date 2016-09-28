---
title: Write Skew
---

The page on collisions showed that if two transactions overlap and write the same data then one will
fail.  However, in the case where two transactions overlap and one reads data that another is writing
then both can succeed.  This behavior is called write skew.

The example below shows write skew.  In the example *n0* is a node in a tree with two children *n01*
and *n02*.  In *tx2* the sum of *n0* is set to the sum of its children.  However *tx2* misses the
concurrent update from *tx3*.  Both *tx2* and *tx3* will commit successfully since they write to
different keys.

 * **Create transaction** *tx1*
 * **Using** *tx1* **set** *n0:data:sum* **to** *0*
 * **Using** *tx1* **set** *n01:data:sum* **to** *1*
 * **Using** *tx1* **set** *n02:data:sum* **to** *2*
 * **Commit** *tx1*
 * **Create transaction** *tx2*
 * **Create transaction** *tx3*
 * **Using** *tx2* **set** *n0:data:sum* **to the value of** *n01:data:sum* **plus** *n02:data:sum*
 * **Using** *tx3* **set** *n01:data:sum* **to** *5*
 * **Commit** *tx2*
 * **Commit** *tx3*
 * **Create snapshot and print** *n0:data:sum*, *n01:data:sum*, **and** *n02:data:sum*

The changes made by *tx3* will not be seen by *tx2*. This behavior is OK if the update made by *tx3*
triggers a later update of *n0:data:sum*. Later pages in the tour will show that Observers can work
this way, so that eventually the changes made by *tx3* are incorporated.  The [Weak Notification
Exercise](/tour/weak-notifications/) later in the tour shows an example of an Observer that works
like this.
