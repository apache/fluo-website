---
title: Data Model
---

Fluo uses Accumulo's data model which is based on the BigTable data model.
This data model supports a large online sorted map that spans multiple nodes in
a cluster.   The keys in this map have four components : row, column family,
column qualifier, and column visibility.

 * **Row** : This portion of the key is used to partition data across nodes in
   a cluster.  All data in a row is guaranteed to be stored on single node in
   the cluster.  Different rows may be stored on different nodes.  Fluo
   supports cross row transactions, which mean cross node transactions.
 * **Column family** :  This portion of the key is used to partition data
   within each node on the cluster.  The data model has locality groups which
   store column families in physically separate partitions on each node.  If
   locality groups are configured, then it allows scanning a subset of rows column
   families much more quickly.
 * **Column Qualifier** : This portion of the key is used to define arbitrary
   columns within a column family.
 * **Column Visibility** : In Accumulo this portion of the key is used to
   control access to data.

This data model is schema-less, there is no need to predefine columns.  One
thing that's defined in the Accumulo data modes that's not available in Fluo is
timestamps.  When using Fluo the timestamp portion of the key is not available.

In the subsequent pages of the tour the shorthand *\<row\>:\<family\>:\<qualifier\>*
will be used.  For example, the following ...

```
row       = kerbalnaut001
family    = name
qualifier = last
```

... would be written as *kerbalnaut001:name:last*.
