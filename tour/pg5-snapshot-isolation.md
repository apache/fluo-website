Snapshot Isolation
------------------

Fluo provides Snapshot isolation.  This means that a Transaction or Snapshot
can only see what was commited before it started.   The following steps
demonstrate the concept of snapshot isolation. Try to code up the steps using
Fluo, then run it and see if it prints what you expect.  If there is something
you are unsure about, code for the following steps is on the next page.


 * Create transaction *tx1*
 * Using *tx1* set row=kerbalnaut0001 fam=name qual=last to Kerbin
 * Commit *tx1*
 * Create transaction *tx2*
 * Using *tx2* set row=kerbalnaut0001 fam=name qual=last to Kerman
 * Create snapshot *s1*
 * Commit *tx2*
 * Create snapshot *s2*
 * Using *s1* print row=kerbalnaut0001 fam=name qual=last
 * Using *s2* print row=kerbalnaut0001 fam=name qual=last
