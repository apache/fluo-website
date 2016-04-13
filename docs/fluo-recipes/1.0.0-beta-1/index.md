---
layout: page
title: Fluo Recipes 1.0.0-beta-1 Documentation
---

**Please Note** - This documentation is for an old Fluo Recipes release.  Documentation for all releases can be found [here](/docs/)

Common code for Fluo application developers.  

### Available Recipes

* [Collision Free Map][cfm] - A recipe for making many to many updates.
* [Export Queue][export-q] - A recipe for exporting data from Fluo to external systems.
* [RecordingTransaction][recording-tx] - A wrapper for a Fluo transaction that records all transaction
operations to a log which can be used to export data from Fluo.

### Common Functionality

Recipes have common needs that are broken down into the following reusable components.

* [Serialization][serialization] - Common code for serializing POJOs. 
* [Transient Ranges][transient] - Standardized process for dealing with transient data.
* [Table optimization][optimization] - Standardized process for optimizing the Fluo table.

[cfm]: /docs/fluo-recipes/1.0.0-beta-1/cfm/
[export-q]: /docs/fluo-recipes/1.0.0-beta-1/export-queue/
[recording-tx]: /docs/fluo-recipes/1.0.0-beta-1/recording-tx/
[serialization]: /docs/fluo-recipes/1.0.0-beta-1/serialization/
[transient]: /docs/fluo-recipes/1.0.0-beta-1/transient/
[optimization]: /docs/fluo-recipes/1.0.0-beta-1/table-optimization/
