---
title: Apache Fluo Recipes 1.1.0-incubating released
date: 2017-06-22 10:30:00 +0000
version: fluo-recipes-1.1.0-incubating
---

Apache Fluo Recipes builds on the Apache Fluo API to provide libraries of common code for Fluo developers.

Below are resources for this release:

 * Download a release tarball and verify by these [procedures] using these [KEYS]

   | [fluo-recipes-1.1.0-incubating-source-release.tar.gz][src-release] | [ASC][src-asc] [MD5][md5] [SHA][sha] |

* View the [documentation][docs]
* Read the javadocs: <a href="{{ site.api_base }}/fluo-recipes-core/1.1.0-incubating/" target="_blank">core</a>, <a href="{{ site.api_base }}/fluo-recipes-accumulo/1.1.0-incubating/" target="_blank">accumulo</a>, <a href="{{ site.api_base }}/fluo-recipes-kryo/1.1.0-incubating/" target="_blank">kryo</a>, <a href="{{ site.api_base }}/fluo-recipes-spark/1.1.0-incubating/" target="_blank">spark</a>, <a href="{{ site.api_base }}/fluo-recipes-test/1.1.0-incubating/" target="_blank">test</a>
* Jars are available in [Maven Central][central].
* View the [changes].

## Major Change

For this release of Fluo Recipes, supporting the [new Observer API][obsAPI] was
the primary motivation.  The Collision Free Map and [Export Queue] required
significant additions to support the new Observer API.  Since the name
*Collision Free Map* (CFM) is awful and it needed major API additions, the
decision was made to deprecate it and offer the [CombineQueue].  The
CombineQueue offers the  same functionality as the CFM, but only supports the
new observer API. The deprecated CFM still supports the old Observer API.  For
the Export Queue, additions were made to its API and everything related to the
old Observer API was deprecated.  All API changes in this release are backwards
compatible with the 1.0.0 release.

### Example of new APIs

The new APIs in this release are much easier to use and now offer the ability
to use lambdas.  This example attempts to shows this and does the following :
 
 * Counts events in three dimensions `(x,y,t)`.
 * Counts events in the two dimensional cross sections : `(x,y)`, `(x,t)`, and `(y,t)`.   
 * Prints out the counts as they change.

To illustrate what this example accomplishes, for the following inputs :

 * `2` events at `(x=3,y=3,t=5)`
 * `1` events at `(x=3,y=3,t=5)`
 * `4` events at `(x=7,y=3,t=5)`

The example code should compute the following.

 * `3` events at `(x=3,y=3,t=5)`
 * `4` events at `(x=7,y=3,t=5)`
 * `3` events at `(x=3,y=3)`
 * `4` events at `(x=7,y=3)`
 * `3` events at `(x=3,t=5)`
 * `4` events at `(x=7,t=5)`
 * `7` events at `(y=3,t=5)`

The example achieves this using recipes as follows :

 * An export queue that prints out all changes in counts.
 * Three combine queues for counting 2D cross sections.  All three queue data for export when counts change.
 * A combine queue for counting 3D events.  It queues updates to the 2D combine queues when counts changes.  It also queues changes to the export queue.

Below is the Fluo [ObserverProvider] that wires everything together. The new
Fluo and Fluo Recipes APIs enable wiring everything in Java code.  In the
previous versions, this would have been a cumbersome combination of
configuration and Java code.   With the new APIs, using lambdas is now an
option.  This was not an option with the old APIs.

```java
public class AppObserverProvider implements ObserverProvider {

  @Override
  public void provide(Registry obsRegistry, Context ctx) {
    SimpleConfiguration appCfg = ctx.getAppConfiguration();

    CombineQueue<String, Long> xytCq = CombineQueue.getInstance(Example.CQ_XYT_ID, appCfg);
    CombineQueue<String, Long> xyCq = CombineQueue.getInstance(Example.CQ_XY_ID, appCfg);
    CombineQueue<String, Long> ytCq = CombineQueue.getInstance(Example.CQ_YT_ID, appCfg);
    CombineQueue<String, Long> xtCq = CombineQueue.getInstance(Example.CQ_XT_ID, appCfg);

    ExportQueue<String, String> exportQ = ExportQueue.getInstance(Example.EXPORTQ_ID, appCfg);

    // Some of Lambda's below could be inlined. To make the example a little more clear they were
    // not in order to show the types involved.

    // This is called by a combine queue when a value changes. The old and new value for the key
    // are passed. The lambda below queues changes for export.
    ChangeObserver<String, Long> expChangeObs = (tx, changes) -> {
      for (Change<String, Long> change : changes) {
        String oldVal = change.getOldValue().map(v -> "old: " + v).orElse("old: -");
        String newVal = change.getNewValue().map(v -> "new: " + v).orElse("new: -");
        exportQ.add(tx, change.getKey(), oldVal + " " + newVal);
      }
    };

    // This lambda processes changes to 3D counts. It queues updates to the (x,y), (x,t), and (y,t)
    // 2D combine queues. For example if (x=3,y=2,t=5) changed from 4 to 7, it would queue
    // (x=3,y=2):+3, (x=3,t=5):+3, and (y=2,t=5):+3 to the 2D combine queues. The lambda also queues
    // exports for 3D count changes.
    ChangeObserver<String, Long> projectingChangeObs = (tx, changes) -> {
      Map<String, Long> xtUpdates = new HashMap<>();
      Map<String, Long> ytUpdates = new HashMap<>();
      Map<String, Long> xyUpdates = new HashMap<>();

      for (Change<String, Long> change : changes) {
        String[] fields = change.getKey().split(":");
        long delta = change.getNewValue().orElse(0L) - change.getOldValue().orElse(0L);

        // While processing the changes for an entire bucket, opportunistically merge multiple
        // updates to the same 2D coordinates.
        xtUpdates.merge(fields[0] + ":" + fields[2], delta, Long::sum);
        ytUpdates.merge(fields[1] + ":" + fields[2], delta, Long::sum);
        xyUpdates.merge(fields[0] + ":" + fields[1], delta, Long::sum);
      }

      // Queue updates to 2D combine queues.
      xtCq.addAll(tx, xtUpdates);
      ytCq.addAll(tx, ytUpdates);
      xyCq.addAll(tx, xyUpdates);

      // Queue changes for export
      expChangeObs.process(tx, changes);
    };

    // Register observer for 3D combine queue. The observer calls the provided combiner and
    // change observer when processing queued entries.
    xytCq.registerObserver(obsRegistry, new SummingCombiner<>(), projectingChangeObs);

    // Register observers for all 2D combine queues.
    xyCq.registerObserver(obsRegistry, new SummingCombiner<>(), expChangeObs);
    xtCq.registerObserver(obsRegistry, new SummingCombiner<>(), expChangeObs);
    ytCq.registerObserver(obsRegistry, new SummingCombiner<>(), expChangeObs);

    // This functional interface is new in this release. The lambda below prints out data that was
    // successfully queued for export.
    Exporter<String, String> exporter = iter -> {
      while (iter.hasNext()) {
        SequencedExport<String, String> seqExport = iter.next();
        System.out.printf("EXPORT %-15s %-15s seq: %d\n", seqExport.getKey(), seqExport.getValue(),
            seqExport.getSequence());
      }
    };

    // Register an observer to process queued export entries. The observer will call the lambda
    // created above.
    exportQ.registerObserver(obsRegistry, exporter);
  }
}
```

The code below does three things :

 * Starts MiniFluo.
 * Configures the four combine queues and the export queue.
 * Adds some data to the 3D combine queue twice.  Between the adds, it waits for processing to finish.
 
```java
    FluoConfiguration props = new FluoConfiguration();
    props.setApplicationName("dimensions");
    props.setMiniDataDir("target/mini");

    CombineQueue.configure(CQ_XYT_ID).keyType(String.class).valueType(Long.class).buckets(7).save(props);
    CombineQueue.configure(CQ_XT_ID).keyType(String.class).valueType(Long.class).buckets(7).save(props);
    CombineQueue.configure(CQ_XY_ID).keyType(String.class).valueType(Long.class).buckets(7).save(props);
    CombineQueue.configure(CQ_YT_ID).keyType(String.class).valueType(Long.class).buckets(7).save(props);

    // A new Fluent method of configuring export queues was introduced in 1.1.0
    ExportQueue.configure(EXPORTQ_ID).keyType(String.class).valueType(String.class).buckets(7).save(props);

    props.setObserverProvider(AppObserverProvider.class);

    FileUtils.deleteQuietly(new File("target/mini"));

    try (MiniFluo miniFluo = FluoFactory.newMiniFluo(props); 
         FluoClient fc = FluoFactory.newClient(miniFluo.getClientConfiguration())) {

      CombineQueue<String,Long> xytCq = CombineQueue.getInstance(CQ_XYT_ID, fc.getAppConfiguration());

      Map<String,Long> updates = new HashMap<>();
      updates.put("x=3:y=5:t=23", 1L);
      updates.put("x=5:y=5:t=27", 1L);
      updates.put("x=3:y=5:t=27", 1L);

      try (Transaction tx = fc.newTransaction()) {
        xytCq.addAll(tx, updates);
        tx.commit();
      }

      miniFluo.waitForObservers();
      System.out.println("\n*** All notifications processed. ***\n");

      updates.clear();
      updates.put("x=3:y=5:t=23", 1L);
      updates.put("x=5:y=5:t=27", -1L);
      updates.put("x=3:y=5:t=29", 1L);

      try (Transaction tx = fc.newTransaction()) {
        xytCq.addAll(tx, updates);
        tx.commit();
      }

      miniFluo.waitForObservers();
      System.out.println("\n*** All notifications processed. ***\n");
    }
```

Below is the output of running this example.

```
EXPORT x=3:y=5:t=23    old: - new: 1   seq: 8
EXPORT x=3:y=5:t=27    old: - new: 1   seq: 9
EXPORT x=5:y=5:t=27    old: - new: 1   seq: 9
EXPORT x=3:y=5         old: - new: 2   seq: 37
EXPORT y=5:t=27        old: - new: 2   seq: 42
EXPORT x=3:t=23        old: - new: 1   seq: 36
EXPORT x=5:t=27        old: - new: 1   seq: 36
EXPORT x=3:t=27        old: - new: 1   seq: 38
EXPORT x=5:y=5         old: - new: 1   seq: 39
EXPORT y=5:t=23        old: - new: 1   seq: 41

*** All notifications processed. ***

EXPORT x=3:y=5:t=29    old: - new: 1   seq: 92
EXPORT x=5:y=5:t=27    old: 1 new: -   seq: 92
EXPORT x=3:y=5:t=23    old: 1 new: 2   seq: 93
EXPORT y=5:t=27        old: 2 new: 1   seq: 109
EXPORT x=3:y=5         old: 2 new: 4   seq: 110
EXPORT y=5:t=23        old: 1 new: 2   seq: 111
EXPORT y=5:t=29        old: - new: 1   seq: 108
EXPORT x=3:t=29        old: - new: 1   seq: 105
EXPORT x=3:t=23        old: 1 new: 2   seq: 106
EXPORT x=5:y=5         old: 1 new: -   seq: 107
EXPORT x=5:t=27        old: 1 new: -   seq: 106

*** All notifications processed. ***
```


[procedures]: https://www.apache.org/info/verification
[KEYS]: https://www.apache.org/dist/incubator/fluo/KEYS
[src-release]: https://www.apache.org/dyn/closer.lua/incubator/fluo/fluo-recipes/1.1.0-incubating/fluo-recipes-1.1.0-incubating-source-release.tar.gz
[src-asc]: https://www.apache.org/dist/incubator/fluo/fluo-recipes/1.1.0-incubating/fluo-recipes-1.1.0-incubating-source-release.tar.gz.asc
[md5]: https://www.apache.org/dist/incubator/fluo/fluo-recipes/1.1.0-incubating/fluo-recipes-1.1.0-incubating-source-release.tar.gz.md5
[sha]: https://www.apache.org/dist/incubator/fluo/fluo-recipes/1.1.0-incubating/fluo-recipes-1.1.0-incubating-source-release.tar.gz.sha
[docs]: /docs/fluo-recipes/1.1.0-incubating
[central]: http://search.maven.org/#search|ga|1|fluo-recipes
[changes]: https://github.com/apache/incubator-fluo-recipes/milestone/1?closed=1
[obsAPI]: /release/fluo-1.1.0-incubating/#new-api-for-configuring-observers
[ObserverProvider]: {{ site.fluo_api_static }}/1.1.0-incubating/org/apache/fluo/api/observer/ObserverProvider.html
[CombineQueue]: {{ site.fluo_recipes_core_static }}/1.1.0-incubating/org/apache/fluo/recipes/core/combine/CombineQueue.html
[Export Queue]: {{ site.fluo_recipes_core_static }}/1.1.0-incubating/org/apache/fluo/recipes/core/export/ExportQueue.html
