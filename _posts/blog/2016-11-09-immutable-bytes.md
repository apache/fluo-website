---
title: "Java needs an immutable byte string"
date: 2016-11-10 11:43:00 +0000
author: Keith Turner
reviewers: Christopher Tubbs, Mike Walch
---

## Fluo Data Model and Transactions

Fluo uses a [data model][dm] composed of key/values.  Each key has four fields :
*row*,*family*,*qualifier*,*visibility*.  Each of these key fields is a sequence of bytes.  Fluo
transactions read key/values from a snapshot of a table.  Any changes a transaction makes is
buffered until commit.  At the time of commit the changes are only made if no other transaction
modified any of the key values.

While designing the Fluo API we were uncertain about making Fluo's basic [POJOs] mutable or
immutable.  In the end we decided to go with immutable types to make writing correct Fluo code
easier.  One of the POJOs we created was [Bytes],  an immutable wrapper around a byte array.  We
also created [BytesBuilder], which is analagous to StringBuilder, and makes it easy and efficient
to construct Bytes.

### What about the copies?

Bytes requires a defensive copy at creation time.  When we were designing Fluo's API we were worried
about this at first.  However a simple truth became apparent.  If the API took a mutable type, then
all boundary points between the user and Fluo would require defensive copies.  For example assume
Fluo's API took byte arrays and consider the following code.

```java
//A Fluo transaction
Transaction tx = ...
byte[] row = ...

tx.set(row, column1, value1);
tx.set(row, column2, value2);
tx.set(row, column3, value3);
```

Fluo will buffer changes until a transaction is committed.  In the example above since Fluo accepts
a mutable row, it would be prudent to do a defensive copy each time `set()` is called above.

In the code below where an immutable byte array wrapper is used, the calls to `set()` do not need to
do a defensive copy.  So when comparing the two examples, the immutable byte wrapper results in less
defensive copies.

```java
//A Fluo transaction
Transaction tx = ...
Bytes row = ...

tx.set(row, column1, value1);
tx.set(row, column2, value2);
tx.set(row, column3, value3);
```

We really did not want to create Bytes and BytesBuilder types, however we could not find what we
needed in Java's standard libraries.  The following sections discuss some of the options we
considered.

## Why not use String?

Java's String type is an immutable wrapper around a char array.  In order to store a byte array in a
String, Java must decode the byte array using a character set.  Some sequences of bytes do not map
in some characters sets.  Therefore, trying to stuff arbitrary binary data in a String can corrupt
the data.  The following little program shows this, it will print `false`.

```java
    byte bytes1[] = new byte[256];
    for(int i = 0; i<255; i++)
      bytes1[i] = (byte)i;

    byte bytes2[] = new String(bytes1).getBytes();

    System.out.println(Arrays.equals(bytes1, bytes2));
```

String can be made to work by specifying an appropriate character set. The following program will
print `true`.  However, this is error prone and inefficient.  It's error prone in the case where the
character set is wrong or omitted.  It's inefficient because it results in copying from byte arrays
to char arrays and visa versa.  Also, char arrays use twice as much memory.

```java
    byte bytes1[] = new byte[256];
    for(int i = 0; i<255; i++)
      bytes1[i] = (byte)i;

    String str = new String(bytes1, StandardCharsets.ISO_8859_1);
    byte bytes2[] = str.getBytes(StandardCharsets.ISO_8859_1);

    System.out.println(Arrays.equals(bytes1, bytes2));
```

## Why not use ByteBuffer?

A read only ByteBuffer might seem like it would fit the bill of an immutable byte array wrapper.
However, the following program shows two ways that ByteBuffer falls short.  ByteBuffers are great
for I/O, but it would not be prudent to use them when immutability is desired.

```java
    byte[] bytes1 = new byte[] {1,2,3,(byte)250};
    ByteBuffer bb1 = ByteBuffer.wrap(bytes1).asReadOnlyBuffer();

    System.out.println(bb1.hashCode());
    bytes1[2]=89;
    System.out.println(bb1.hashCode());
    bb1.get();
    System.out.println(bb1.hashCode());
```

The program above prints the following, which is less than ideal :

```
747721
830367
26786
```

This little program shows two things.  First, the only guarantee we are getting from
`asReadOnlyBuffer()` is that `bb1` can not be used to modify `bytes1`.  However, the originator of
the read only buffer can still modify the wrapped byte array.   Java's String and Fluo's Bytes avoid
this by always copying data into an internal private array that never escapes.

The second issue is that `bb1` has a position and calling `bb1.get()` changes this position.
Changing the position conceptually changes the contents of the ByteBuffer.  This is why `hashCode()`
returns something different after `bb1.get()` is called.  So even though `bb1` does not enable
mutating `bytes1`, `bb1` is itself mutable.

## Why not use Protobuf's ByteString?

[Protocol Buffers][pb] has a beautiful implementation of an immutable byte array wrapper called
[ByteString].  I would encourage its use when possible.  I discovered this jewel after Bytes was
implemented in Fluo.  Using it was considered, however in Fluo's case its not really appropriate to
use for two reasons.  First, any library designer should try to minimize what transitive dependencies
they force on users.  Internally Fluo does not currently use Protocol Buffers in its implementation,
so this would be a new dependency for Fluo users.  The second reason is going to require some
background to explain.

Technologies like [OSGI] and [Jigsaw] seek to modularize Java libraries and provide dependency
isolation.  Dependency isolation allows a user to use a library without having to share a libraries
dependencies.  For example, consider the following hypothetical scenario.

 * Fluo's implementation uses Protobuf version 2.5
 * Fluo user code uses Protobuf version 1.8

Without dependency isolation, the user must converge dependencies and make their application and
Fluo use the same version of Protobuf.  Sometimes this works without issue, but sometimes things
will break because Protobuf dropped, changed, or added a method.

With dependency isolation, Fluo's implementation and Fluo user code can easily use different versions
of Protobuf.  This is only true as long as Fluo's API does not use Protobuf.  So, this is the second
reason that Fluo should not use classes from Protobuf in its API.  If Fluo used Protobuf in its API
then it forces the user to have to converge dependencies, even if they are using OSGI or Jigsaw.

## Java should have an immutable byte array wrapper

So far, the following arguments have been presented:

 * An immutable byte array wrapper is useful and needed.
 * Java does not provide a good immutable byte array wrapper.
 * Using an immutable byte array wrapper from library X in library Y's API may be problematic.

These arguments all point to the need for an immutable byte array wrapper to exist in Java. This
need could also be satisfied by a library outside of Java with some restrictions. Assume a new
library called Lib Immutable Byte Array Wrapper (libibaw) was created.  In order for libibaw to be
used in other libraries APIs, it would need to promise the following.

 * No dependencies other than Java.
 * Backwards compatibility.

The reason backwards compatibility is important is that it would make dependency convergence super
easy.  The following situation shows this.

 * Fluo uses libibaw 1.2 in its API
 * Fluo user code uses libibaw 1.1.

If libibaw promises backward compatibility, then all the user needs to do is use version 1.2 of
libibaw.  With the promise of backwards compatibility, using version 1.2 will not break the users
code.

Having a library would be nice, but having something in Java would minimize copies.  Outside
of Java there will inevitably be multiple implementations and going between them will require a
copy.  For example if a user uses Fluo and Protobuf they may be forced to copy Fluo's Bytes to
Protobuf's ByteString. If Protobuf and Fluo both used an immutable byte sequence type from Java, this
would not be needed.

[Bytes]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/data/Bytes.html
[BytesBuilder]: {{ site.fluo_api_static }}/{{ site.latest_fluo_release }}/org/apache/fluo/api/data/Bytes.BytesBuilder.html
[ByteString]: https://developers.google.com/protocol-buffers/docs/reference/java/com/google/protobuf/ByteString
[pb]: https://developers.google.com/protocol-buffers/
[OSGI]: https://www.osgi.org
[JigSaw]: http://openjdk.java.net/projects/jigsaw/
[dm]: /tour/data-model/
[POJOs]: /tour/data-pojos/
