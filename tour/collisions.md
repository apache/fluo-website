---
title: Collisions
---

When two transactions overlap and attempt to modify the same data, one of them
will fail.  Try writing code to do the following which will create a collision.

 * **Create transaction** *tx1*
 * **Using** *tx1* **set** *kerbalnaut0001:name:last* **to** *Kerma*
 * **Commit** *tx1*
 * **Create transaction** *tx2*
 * **Create transaction** *tx3*
 * **Using** *tx2* **append** *n* **to the value of** *kerbalnaut0001:name:last*
 * **Using** *tx3* **append** *N* **to the value of** *kerbalnaut0001:name:last*
 * **Commit** *tx2*
 * **Commit** *tx3* **wrapping with try/catch that prints Exception**
 * **Create snapshot and print** *kerbalnaut0001:name:last*
