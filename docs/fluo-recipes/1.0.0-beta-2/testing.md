---
layout: recipes-doc
title: Testing
version: 1.0.0-beta-2
---
Fluo includes MiniFluo which makes it possible to write an integeration test that
runs against a real Fluo instance.  Fluo Recipes provides the following utility
code for writing an integration test.

 * [FluoITHelper][1] A class with utility methods for comparing expected data with whats in Fluo.
 * [AccumuloExportITBase][2] A base class for writing an integration test that exports data from Fluo to an external Accumulo table.

[1]: {{ site.old_api_static }}/fluo-recipes-test/1.0.0-beta-2/io/fluo/recipes/test/FluoITHelper.html
[2]: {{ site.old_api_static }}/fluo-recipes-test/1.0.0-beta-2/io/fluo/recipes/test/AccumuloExportITBase.html
