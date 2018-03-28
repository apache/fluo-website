---
title: Read Locks
---

By default, reads do not acquire a lock which makes normal reads faster.
Read locks can optionally be acquired via the [withReadLock] method. For
example, if `tx` is a transaction then `tx.withReadLock().get(row,col)`
reads with a lock.


 * **Create transaction** *tx1*
 * **Using** *tx1* **set** *kerbalnaut0001:stat:weight* **to** *90*
 * **Using** *tx1* **set** *kerbalnaut0002:stat:weight* **to** *70*
 * **Using** *tx1* **set** *kerbalnaut0003:stat:weight* **to** *80*
 * **Commit** *tx1*
 * **Create transaction** *tx2*
 * **Create transaction** *tx3*
 * **Create transaction** *tx4*
 * **Using** *tx2* **set** *flight0001:stat:weight* **to the read locked values of** *kerbalnaut0001:stat:weight* **plus** *kerbalnaut0003:stat:weight*
 * **Using** *tx3* **set** *flight0002:stat:weight* **to the read locked values of** *kerbalnaut0001:stat:weight* **plus** *kerbalnaut0002:stat:weight*
 * **Using** *tx4* **set** *kerbalnaut0001:stat:weight* **to** *95*
 * **Commit** *tx2*
 * **Commit** *tx3*
 * **Commit** *tx4*

Both *tx2* and *tx3* get a read lock on *kerbalnaut0001:stat:weight* without
interfering with each other.  The read locks prevent *tx4* from committing.
Try reordering the commits for *tx2*, *tx3*, and *tx4*.

[withReadLock]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/TransactionBase.html#withReadLock--
