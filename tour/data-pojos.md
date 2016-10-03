---
title: Basic Data Types
---

Fluo has a few simple POJOs that are used throughout the API.  These classes
are found in [org.apache.fluo.api.data][data-pkg].  All of these types are
immutable. Except for Span, all of the types are Comparable and have hash
code and equals implementations.  These types work with [Bytes] and Java
Strings.  Internally, Fluo only works with bytes.  All API methods that deal
with String will convert back and forth to and from bytes using UTF-8.

[Bytes] is modeled after Java String.  Its an immutable wrapper around `byte[]`
like String is an immutable wrapper around `char[]`.  To make building [Bytes]
more efficient and easier, there is a reusable [BytesBuilder] that is modeled
after StringBuilder.  Call [Bytes.builder()][nb] to create a new [BytesBuilder].

[data-pkg]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/data/package-summary.html
[Bytes]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/data/Bytes.html
[BytesBuilder]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/data/Bytes.BytesBuilder.html
[nb]: /apidocs/fluo/{{ site.latest_fluo_release }}/org/apache/fluo/api/data/Bytes.html#builder--

