---
title: Transaction Logging
---

Fluo can produce detailed logs about transactions if configured to do so.
This can be useful for debugging.  Modify `./src/main/resources/log4j.properties`
and remove `#` on the line `#log4j.logger.fluo.tx=TRACE`.  After doing this,
rerun the collision exercise on the previous page.

With this configuration change, you should see output like the following.
Notice the logging shows what was read, set, and the collision information.

```
Starting MiniFluo ... started.
TRACE: txid: 3 begin() thread: 10
TRACE: txid: 3 set(kerbalnaut0001, name last , Kerma)
TRACE: txid: 3 commit() -> SUCCESSFUL commitTs: 4
TRACE: txid: 3 close()
TRACE: txid: 3 thread : 10 time: ... #ret: 0 #set: 1 #collisions: 0 waitTime: 0 committed: true class: N/A
TRACE: txid: 5 begin() thread: 10
TRACE: txid: 6 begin() thread: 10
TRACE: txid: 5 get(kerbalnaut0001, name last ) -> Kerma
TRACE: txid: 5 set(kerbalnaut0001, name last , Kerman)
TRACE: txid: 6 get(kerbalnaut0001, name last ) -> Kerma
TRACE: txid: 6 set(kerbalnaut0001, name last , KermaN)
TRACE: txid: 5 commit() -> SUCCESSFUL commitTs: 7
TRACE: txid: 6 commit() -> UNSUCCESSFUL commitTs: -1
TRACE: txid: 6 collisions: {kerbalnaut0001=[name last ]}
tx3 commit exception : org.apache.fluo.api.exceptions.CommitException
TRACE: txid: 6 close()
TRACE: txid: 6 thread : 10 time: ... #ret: 1 #set: 1 #collisions: 1 waitTime: 0 committed: false class: N/A
TRACE: txid: 5 close()
TRACE: txid: 5 thread : 10 time: ... #ret: 1 #set: 1 #collisions: 0 waitTime: 0 committed: true class: N/A
TRACE: txid: 8 begin() thread: 10
TRACE: txid: 8 get(kerbalnaut0001, name last ) -> Kerman
Kerman
TRACE: txid: 8 close()
TRACE: txid: 8 thread : 10 time: ... #ret: 1 #set: 0 #collisions: 0 waitTime: 0 committed: false class: N/A
```

More information about configuring logging is available in [the logging
documentation](/docs/fluo/{{ site.latest_fluo_minor }}/administration/manage-applications#debugging-applications).
