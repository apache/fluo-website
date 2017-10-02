---
title: Accumulo Export
category: recipes
order: 3
---

## Background

The [Export Queue Recipe][1] provides a generic foundation for building export mechanism to any
external data store. The [AccumuloExporter] provides an [Exporter] for writing to
Accumulo. [AccumuloExporter] is located in the `fluo-recipes-accumulo` module and provides the
following functionality:

 * Safely batches writes to Accumulo made by multiple transactions exporting data.
 * Stores Accumulo connection information in Fluo configuration, making it accessible by Export
   Observers running on other nodes.
 * Provides utility code that make it easier and shorter to code common Accumulo export patterns.

## Example Use

Exporting to Accumulo is easy. Follow the steps below:

1.  First, implement [AccumuloTranslator].  Your implementation translates exported
    objects to Accumulo Mutations. For example, the `SimpleTranslator` class below translates String
    key/values and into mutations for Accumulo.  This step is optional, a lambda could
    be used in step 3 instead of creating a class.

    ```java
    public class SimpleTranslator implements AccumuloTranslator<String,String> {

      @Override
      public void translate(SequencedExport<String, String> export, Consumer<Mutation> consumer) {
        Mutation m = new Mutation(export.getKey());
        m.put("cf", "cq", export.getSequence(), export.getValue());
        consumer.accept(m);
      }
    }
    ```

2.  Configure an `ExportQueue` and the export table prior to initializing Fluo.

    ```java
    FluoConfiguration fluoConfig = ...;

    String instance =       // Name of accumulo instance exporting to
    String zookeepers =     // Zookeepers used by Accumulo instance exporting to
    String user =           // Accumulo username, user that can write to exportTable
    String password =       // Accumulo user password
    String exportTable =    // Name of table to export to

    // Set properties for table to export to in Fluo app configuration.
    AccumuloExporter.configure(EXPORT_QID).instance(instance, zookeepers)
        .credentials(user, password).table(exportTable).save(fluoConfig);

    // Set properties for export queue in Fluo app configuration
    ExportQueue.configure(EXPORT_QID).keyType(String.class).valueType(String.class)
        .buckets(119).save(fluoConfig);

    // Initialize Fluo using fluoConfig
    ```

3.  In the applications `ObserverProvider`, register an observer that will process exports and write
    them to Accumulo using [AccumuloExporter].  Also, register observers that add to the export
    queue.

    ```java
    public class MyObserverProvider implements ObserverProvider {

      @Override
      public void provide(Registry obsRegistry, Context ctx) {
        SimpleConfiguration appCfg = ctx.getAppConfiguration();

        ExportQueue<String, String> expQ = ExportQueue.getInstance(EXPORT_QID, appCfg);

        // Register observer that will processes entries on export queue and write them to the Accumulo
        // table configured earlier. SimpleTranslator from step 1 is passed here, could have used a
        // lambda instead.
        expQ.registerObserver(obsRegistry,
            new AccumuloExporter<>(EXPORT_QID, appCfg, new SimpleTranslator()));

        // An example observer created using a lambda that adds to the export queue.
        obsRegistry.forColumn(OBS_COL, WEAK).useObserver((tx,row,col) -> {
          // Read some data and do some work

          // Add results to export queue
          String key =    // key that identifies export
          String value =  // object to export
          expQ.add(tx, key, value);
        });
      }
    }
    ```

## Other use cases

The `getTranslator()` method in [AccumuloReplicator] creates a specialized [AccumuloTranslator] for replicating a Fluo table to Accumulo.

[1]: {{ page.docs_base }}/recipes/export-queue/
[Exporter]: {{ page.javadoc_core }}/org/apache/fluo/recipes/core/export/function/Exporter.html
[AccumuloExporter]: {{ page.javadoc_accumulo }}/org/apache/fluo/recipes/accumulo/export/function/AccumuloExporter.html
[AccumuloTranslator]: {{ page.javadoc_accumulo }}/org/apache/fluo/recipes/accumulo/export/function/AccumuloTranslator.html
[AccumuloReplicator]: {{ page.javadoc_accumulo }}/org/apache/fluo/recipes/accumulo/export/AccumuloReplicator.html

