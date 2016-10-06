---
title: Word count Exercise
---

This excercise gives you an opportunity to use everything you have learned so
far to attempt writing a simple Fluo application.  A bare minimum of code,
along with a conceptual sketch of a solution, is provided to get you started.

The application should compute word counts for unique documents. This
application should do the following.

 * Deduplicate content based on hash
 * Count how many URIs reference content
 * For the unique words in content, update global word counts.
 * When new content is added increment the global counts.
 * When content is no longer referenced by any URIs, decrement the global word counts and delete
   that content.
 * Partition different types of data using row prefixes.  Use *u:* for URIs, use *d:* for document
   content, and use *w:* for word counts.

## Part 1 : Loading data.

The class below is a simple POJO for documents.

```java
package ft;

import com.google.common.hash.Hashing;

public class Document {
  public final String uri;
  public final String content;

  public Document(String uri, String content) {
    this.uri = uri;
    this.content = content;
  }

  public String hash() {
    //use short prefix of hash for example
    return Hashing.sha1().hashString(content).toString().substring(0, 7);
  }
}
```

The following code loads documents into Fluo.  It should do the following :

 * Keep track of the current hash associated with a URI.
 * Deduplicate content based on hash
 * Reference count how many URIs point to content.  Track this information in a column named
   *doc:refc* with a row based on the hash.
 * Track the status of whether content is referenced or unreferenced in a column named *doc:refs*.
   Note *refs* is short for reference status.   When the reference count for content is 0 this
   columns value should be *unreferenced*.  When the reference count is greater than 0, the
   *doc:refs* columns value should be *referenced*.  In a later example, an Observer will watch this
   column.
 * Track the content associated with a hash using the *doc:content* column.

Some of this is implemented below, but not all. The parts that are not done have TODOs.

```java
package ft;

import org.apache.fluo.api.client.Loader;
import org.apache.fluo.api.client.TransactionBase;
import org.apache.fluo.api.data.Column;

public class DocLoader implements Loader {

  private final Document doc;

  public static final Column HASH_COL = new Column("uri", "hash");
  public static final Column REF_COUNT_COL = new Column("doc", "refc");
  public static final Column REF_STATUS_COL = new Column("doc", "refs");
  public static final Column CONTENT_COL = new Column("doc", "content");

  public DocLoader(Document doc) {
    this.doc = doc;
  }

  @Override
  public void load(TransactionBase tx, Context context) throws Exception {
    String newHash = doc.hash();
    String oldHash = tx.gets("u:" + doc.uri, HASH_COL);

    // TODO check if uri already has the same content hash.  If so, then nothing to do.

    // TODO set the new hash associated with the URI

    if (oldHash != null) {
      // TODO decrement the reference count at row "d:"+oldHash
      // TODO set REF_STATUS_COL to "unreferenced" when the reference count goes from 1 to 0. Do
      // this for row "d:"+oldHash
    }

    // TODO increment the reference count for the newHash content.
    // TODO add the new content when the reference count does not exists
    // TODO set REF_STATUS_COL to "referenced" when the reference count for the new content goes
    // from 0 to 1.  Do this for row "d:"+newHash
  }
}
```

Add the following to the ft.Main class.

```java
  // some test data
  private static Document[] docs1 = new Document[] {
      new Document("http://news.com/a23",
          "Jebediah orbits Mun for 35 days.  No power, forgot solar panels."),
      new Document("http://news.com/a24",
          "Bill plans to rescue Jebediah after taking tourist to Minimus.")};

  private static Document[] docs2 = new Document[] {new Document("http://oldnews.com/a23",
      "Jebediah orbits Mun for 35 days.  No power, forgot solar panels.")};

  private static Document[] docs3 = new Document[] {
      new Document("http://news.com/a23",
          "Jebediah orbits Mun for 38 days.  No power, forgot solar panels."),
      new Document("http://news.com/a24",
          "Crisis at KSC.  Tourist stuck at Minimus.  Bill forgot solar panels.")};

  /**
   * Utility method for loading documents and printing out Fluo table after load completes.
   */
  private static void loadAndPrint(MiniFluo mini, FluoClient client, Document[] docs) {

    try (LoaderExecutor loaderExecutor = client.newLoaderExecutor()) {
      for (Document document : docs) {
        loaderExecutor.execute(new DocLoader(document));
      }
    } // this will close loaderExecutor and wait for all load transactions to complete

    //This line is not needed in this step of the excercise.  However the next step will need this
    //line.
    mini.waitForObservers();

    System.out.println("**** begin table dump ****");
    try (Snapshot snap = client.newSnapshot()) {
      snap.scanner().build().forEach(rcv -> System.out.println("  " + rcv));
    }
    System.out.println("**** end table dump ****\n");
  }

  private static void excercise(MiniFluo mini, FluoClient client) {
    loadAndPrint(mini, client, docs1);
    loadAndPrint(mini, client, docs2);
    loadAndPrint(mini, client, docs3);
  }
```

Once the TODOs in the DocLoader class are implemented, running Main should print out the following.

```
**** begin table dump ****
  d:a6c4d1f doc content  Jebediah orbits Mun for 35 days.  No power, forgot solar panels.
  d:a6c4d1f doc refc  1
  d:a6c4d1f doc refs  referenced
  d:cf8ddc0 doc content  Bill plans to rescue Jebediah after taking tourist to Minimus.
  d:cf8ddc0 doc refc  1
  d:cf8ddc0 doc refs  referenced
  u:http://news.com/a23 uri hash  a6c4d1f
  u:http://news.com/a24 uri hash  cf8ddc0
**** end table dump ****

**** begin table dump ****
  d:a6c4d1f doc content  Jebediah orbits Mun for 35 days.  No power, forgot solar panels.
  d:a6c4d1f doc refc  2
  d:a6c4d1f doc refs  referenced
  d:cf8ddc0 doc content  Bill plans to rescue Jebediah after taking tourist to Minimus.
  d:cf8ddc0 doc refc  1
  d:cf8ddc0 doc refs  referenced
  u:http://news.com/a23 uri hash  a6c4d1f
  u:http://news.com/a24 uri hash  cf8ddc0
  u:http://oldnews.com/a23 uri hash  a6c4d1f
**** end table dump ****

**** begin table dump ****
  d:2732ebc doc content  Crisis at KSC.  Tourist stuck at Minimus.  Bill forgot solar panels.
  d:2732ebc doc refc  1
  d:2732ebc doc refs  referenced
  d:6658252 doc content  Jebediah orbits Mun for 38 days.  No power, forgot solar panels.
  d:6658252 doc refc  1
  d:6658252 doc refs  referenced
  d:a6c4d1f doc content  Jebediah orbits Mun for 35 days.  No power, forgot solar panels.
  d:a6c4d1f doc refc  1
  d:a6c4d1f doc refs  referenced
  d:cf8ddc0 doc content  Bill plans to rescue Jebediah after taking tourist to Minimus.
  d:cf8ddc0 doc refc  0
  d:cf8ddc0 doc refs  unreferenced
  u:http://news.com/a23 uri hash  6658252
  u:http://news.com/a24 uri hash  2732ebc
  u:http://oldnews.com/a23 uri hash  a6c4d1f
**** end table dump ****
```

## Part 2 : Computing word counts.

Now that you have data loading, create an observer that watches the reference
status column.  This observer should increment word counts when new content is
referenced and decrement word counts when content is dereferenced.  The
observer should also delete the content when its dereferenced.

Make sure you handle the following scenario correctly.

 * content A becomes referenced
 * content A becomes unreferenced
 * an observer runs on content A

In this situation, word counts were never incremented for content A so there is no need to decrement
the word counts.  One way to handle this is to have a column that tracks if word counts were
incremented.

Below is a skeleton for an observer to compute word counts.

```java
package ft;

import java.util.Arrays;
import java.util.Collection;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import com.google.common.collect.ImmutableSet;
import org.apache.fluo.api.client.TransactionBase;
import org.apache.fluo.api.data.Bytes;
import org.apache.fluo.api.data.Column;
import org.apache.fluo.api.data.RowColumn;
import org.apache.fluo.api.observer.AbstractObserver;

public class ContentObserver extends AbstractObserver {

  public static final Column PROCESSED_COL = new Column("doc", "processed");
  public static final Column WORD_COUNT = new Column("word","docCount");

  /**
   * Utility method to tokenize the content of a document into unique words.
   */
  private Set<String> tokenize(String content) {
    return new HashSet<String>(Arrays.asList(content.split("[ .!,]+")));
  }

  /**
   *  Adds the passed to delta to the values for each word.
   */
  private void adjustCounts(TransactionBase tx, int delta, Set<String> words) {
    // TODO make a single call to get all of the current word counts.  Could use
    //tx.gets(Collection<RowColumn>)

    // TODO for each word, add delta to the current value and set the new value
  }


  @Override
  public void process(TransactionBase tx, Bytes brow, Column col) throws Exception {

    String row = brow.toString();

    Map<Column, String> colVals =
        tx.gets(row, DocLoader.CONTENT_COL, DocLoader.REF_STATUS_COL, PROCESSED_COL);

    String content = colVals.get(DocLoader.CONTENT_COL);
    String status = colVals.get(DocLoader.REF_STATUS_COL);
    String processed = colVals.getOrDefault(PROCESSED_COL, "false");

    // TODO if status is referenced and not already processed the adjustCounts by +1 and set
    // PROCESSED_COL to true

    // TODO is status is unreferenced then delete all columns for content
    // TODO if status is unreferenced and document was processed, then adjust counts by -1
  }


  @Override
  public ObservedColumn getObservedColumn() {
    return new ObservedColumn(DocLoader.REF_STATUS_COL, NotificationType.STRONG);
  }
}
```

Something to think about: why observe the reference status column instead of the reference count
column?

When you are ready to run the observer, modify the `preInit()` method in `ft.Main` to configure the
observer as follows.

```java
  private static void preInit(FluoConfiguration fluoConfig) {
    fluoConfig.addObserver(new ObserverSpecification(ContentObserver.class.getName()));
  }
```

After implementing the Observer, the output of the program should look like the following.

```
**** begin table dump ****
  d:a6c4d1f doc content  Jebediah orbits Mun for 35 days.  No power, forgot solar panels.
  d:a6c4d1f doc processed  true
  d:a6c4d1f doc refc  1
  d:a6c4d1f doc refs  referenced
  d:cf8ddc0 doc content  Bill plans to rescue Jebediah after taking tourist to Minimus.
  d:cf8ddc0 doc processed  true
  d:cf8ddc0 doc refc  1
  d:cf8ddc0 doc refs  referenced
  u:http://news.com/a23 uri hash  a6c4d1f
  u:http://news.com/a24 uri hash  cf8ddc0
  w:35 word docCount  1
  w:Bill word docCount  1
  w:Jebediah word docCount  2
  w:Minimus word docCount  1
  w:Mun word docCount  1
  w:No word docCount  1
  w:after word docCount  1
  w:days word docCount  1
  w:for word docCount  1
  w:forgot word docCount  1
  w:orbits word docCount  1
  w:panels word docCount  1
  w:plans word docCount  1
  w:power word docCount  1
  w:rescue word docCount  1
  w:solar word docCount  1
  w:taking word docCount  1
  w:to word docCount  1
  w:tourist word docCount  1
**** end table dump ****

**** begin table dump ****
  d:a6c4d1f doc content  Jebediah orbits Mun for 35 days.  No power, forgot solar panels.
  d:a6c4d1f doc processed  true
  d:a6c4d1f doc refc  2
  d:a6c4d1f doc refs  referenced
  d:cf8ddc0 doc content  Bill plans to rescue Jebediah after taking tourist to Minimus.
  d:cf8ddc0 doc processed  true
  d:cf8ddc0 doc refc  1
  d:cf8ddc0 doc refs  referenced
  u:http://news.com/a23 uri hash  a6c4d1f
  u:http://news.com/a24 uri hash  cf8ddc0
  u:http://oldnews.com/a23 uri hash  a6c4d1f
  w:35 word docCount  1
  w:Bill word docCount  1
  w:Jebediah word docCount  2
  w:Minimus word docCount  1
  w:Mun word docCount  1
  w:No word docCount  1
  w:after word docCount  1
  w:days word docCount  1
  w:for word docCount  1
  w:forgot word docCount  1
  w:orbits word docCount  1
  w:panels word docCount  1
  w:plans word docCount  1
  w:power word docCount  1
  w:rescue word docCount  1
  w:solar word docCount  1
  w:taking word docCount  1
  w:to word docCount  1
  w:tourist word docCount  1
**** end table dump ****

**** begin table dump ****
  d:2732ebc doc content  Crisis at KSC.  Tourist stuck at Minimus.  Bill forgot solar panels.
  d:2732ebc doc processed  true
  d:2732ebc doc refc  1
  d:2732ebc doc refs  referenced
  d:6658252 doc content  Jebediah orbits Mun for 38 days.  No power, forgot solar panels.
  d:6658252 doc processed  true
  d:6658252 doc refc  1
  d:6658252 doc refs  referenced
  d:a6c4d1f doc content  Jebediah orbits Mun for 35 days.  No power, forgot solar panels.
  d:a6c4d1f doc processed  true
  d:a6c4d1f doc refc  1
  d:a6c4d1f doc refs  referenced
  u:http://news.com/a23 uri hash  6658252
  u:http://news.com/a24 uri hash  2732ebc
  u:http://oldnews.com/a23 uri hash  a6c4d1f
  w:35 word docCount  1
  w:38 word docCount  1
  w:Bill word docCount  1
  w:Crisis word docCount  1
  w:Jebediah word docCount  2
  w:KSC word docCount  1
  w:Minimus word docCount  1
  w:Mun word docCount  2
  w:No word docCount  2
  w:Tourist word docCount  1
  w:at word docCount  1
  w:days word docCount  2
  w:for word docCount  2
  w:forgot word docCount  3
  w:orbits word docCount  2
  w:panels word docCount  3
  w:power word docCount  2
  w:solar word docCount  3
  w:stuck word docCount  1
**** end table dump ****
```

## Part 3 : Using Fluo Recipes

The way to compute word counts above is very prone to transactional collisions. One way to avoid
these collisions is to use the CollisionFreeMap provided in Fluo Recipes. Currently Fluo Recipes is
not released, this section will be updated with more information once it is.
