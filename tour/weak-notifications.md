---
title: Weak Notification Exercise
---

This exercise will use weak notification to update a shared counter. In the example, many threads
will concurrently try to update the counter but collisions will be avoided.

Create an observer that observes column *ntfy:sum* and make it do the following.

 * For the row triggered append `/` and sum everything with that row prefix.  Also delete the rows
   with that prefix.
 * Print the sum.
 * For the triggering row, update the column *sum:total* with the new sum.

Create a loader that does the following and run it 5000 times :

 * Generate a random number in the range [0,10^7-1].  This will be referred to as *\<rand\>*.
 * Add one to *counter001/\<rand\>:sum:update*
 * Weakly notify *counter001:nfty:sum*

After the loader finishes, wait for observers and then print the value for *counter001:sum:total*.
Since weak notifications are not transactional, all of the threads notifying the same row column
should not collide.

One experiment to try is to use a smaller random number range and enable collision logging.  For
example try generating random numbers in the range of [0,99].  
