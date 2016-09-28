---
title: Snapshot Isolation
---

Fluo provides Snapshot isolation.  This means that a Transaction or Snapshot can only see data
committed before it started.   The following steps demonstrate the concept of snapshot isolation. Try
to code up the steps using Fluo, then run it and see if it prints what you expect.  If there is
something you are unsure about, code for the following steps is on the next page.


 * **Create transaction** *tx1*
 * **Using** *tx1* **set** *kerbalnaut0001:name:last* **to** *Kerbin*
 * **Commit** *tx1*
 * **Create transaction** *tx2*
 * **Using** *tx2* **set** *kerbalnaut0001:name:last* **to** *Kerman*
 * **Create snapshot** *s1*
 * **Commit** *tx2*
 * **Create snapshot** *s2*
 * **Using** *s1* **print** *kerbalnaut0001:name:last*
 * **Using** *s2* **print** *kerbalnaut0001:name:last*
