---
title: Memory limits and self notify
---

All modifications made as part of a transaction must fit into memory because the sets and deletes
are buffered in memory until commit.  If there is more data to process that will fit in memory, one
way to handle this is to process some data and self notify.

As an exercise try modifying the [weak notification exercise](/tour/weak-notifications/) and
making it self notify.  Modify the observer such that it does the following :

 * Processes a maximum number of updates.  Could make this configurable using per observer
   configuration.
 * When the max is reached : 
   * Stop processing.
   * Records the stop row.
   * Notify self.
 * Use the row where it previously stopped when creating scan range.
 * Delete the stop row, if it exists, after scanning to the end of the range.
