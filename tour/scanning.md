---
title: Scanning
---

In some situations you may want to read a range of data instead of specific rows and columns.  For
this case Fluo supports [creating scanners][scanner] over ranges.   These scanners implement Java Iterable and
can be used with foreach loops.  Scanners also support reading a subset of columns within a range.

To specify a range, Fluo has a simple POJO called [Span].  The name was chosen so it would not
conflict with Accumulo's Range. [Span] has multiple static helper methods for creating common
ranges, like a range over all rows with a given prefix.  Try the following exercise using scanners.

 * **Create transaction** *tx1*
 * **Using** *tx1* **set** *kerbalnaut0001:name:last* **to** *Kerman*
 * **Using** *tx1* **set** *kerbalnaut0001:name:first* **to** *Jebediah*
 * **Using** *tx1* **set** *kerbalnaut0001:attr:bravery* **to** *5*
 * **Using** *tx1* **set** *kerbalnaut0002:name:last* **to** *Kerman*
 * **Using** *tx1* **set** *kerbalnaut0002:name:first* **to** *Bill*
 * **Using** *tx1* **set** *kerbalnaut0002:attr:bravery* **to** *2*
 * **Using** *tx1* **set** *kerbalnaut0003:name:last* **to** *Kerman*
 * **Using** *tx1* **set** *kerbalnaut0003:name:first* **to** *Bob*
 * **Using** *tx1* **set** *kerbalnaut0003:attr:bravery* **to** *1*
 * **Using** *tx1* **set** *bravery5:id:kerbalnaut0001* **to** *5*
 * **Using** *tx1* **set** *bravery2:id:kerbalnaut0002* **to** *2*
 * **Using** *tx1* **set** *bravery1:id:kerbalnaut0003* **to** *1*
 * **Commit** *tx1*
 * **Create snapshot** *s1*
 * **Using** *s1* **scan and print row** *kerbalnaut0002*
 * **Using** *s1* **scan and print row** *kerbalnaut0002* **and column family** *name*
 * **Using** *s1* **scan rows with prefix** *kerbalnaut* **with columns** *name:first* **and** *attr:bravery*

Scanners also read data using snapshot isolation.  To show this try modifying the exercise above to
change data after *s1* is created but before the scans happen.

[Span]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/data/Span.html
[scanner]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/client/SnapshotBase.html#scanner--
