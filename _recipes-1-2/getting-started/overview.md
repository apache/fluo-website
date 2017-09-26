---
title: Overview
category: getting-started
order: 1
---

Fluo Recipes are common code for Apache Fluo application developers. They build on the
[Fluo API][fluo-api] to offer additional functionality to
developers. They are published separately from Fluo on their own release schedule.
This allows Fluo Recipes to iterate and innovate faster than Fluo (which will maintain
a more minimal API on a slower release cycle). Fluo Recipes offers code to implement
common patterns on top of Fluo's API.  It also offers glue code to external libraries
like Spark and Kryo.

### Usage

The Fluo Recipes project publishes multiple jars to Maven Central for each release.
The `fluo-recipes-core` jar is the primary jar. It is where most recipes live and where
they are placed by default if they have minimal dependencies beyond the Fluo API.

Fluo Recipes with dependencies that bring in many transitive dependencies publish
their own jar. For example, recipes that depend on Apache Spark are published in the
`fluo-recipes-spark` jar.  If you don't plan on using code in the `fluo-recipes-spark`
jar, you should avoid including it in your pom.xml to avoid a transitive dependency on
Spark.

Below is a sample Maven POM containing all possible Fluo Recipes dependencies:

```xml
<properties>
  <fluo-recipes.version>{{ page.version }}</fluo-recipes.version>
</properties>

<dependencies>
  <!-- Required. Contains recipes that are only depend on the Fluo API -->
  <dependency>
    <groupId>org.apache.fluo</groupId>
    <artifactId>fluo-recipes-core</artifactId>
    <version>${fluo-recipes.version}</version>
  </dependency>
  <!-- Optional. Serialization code that depends on Kryo -->
  <dependency>
    <groupId>org.apache.fluo</groupId>
    <artifactId>fluo-recipes-kryo</artifactId>
    <version>${fluo-recipes.version}</version>
  </dependency>
  <!-- Optional. Common code for using Fluo with Accumulo -->
  <dependency>
    <groupId>org.apache.fluo</groupId>
    <artifactId>fluo-recipes-accumulo</artifactId>
    <version>${fluo-recipes.version}</version>
  </dependency>
  <!-- Optional. Common code for using Fluo with Spark -->
  <dependency>
    <groupId>org.apache.fluo</groupId>
    <artifactId>fluo-recipes-spark</artifactId>
    <version>${fluo-recipes.version}</version>
  </dependency>
  <!-- Optional. Common code for writing Fluo integration tests -->
  <dependency>
    <groupId>org.apache.fluo</groupId>
    <artifactId>fluo-recipes-test</artifactId>
    <version>${fluo-recipes.version}</version>
    <scope>test</scope>
  </dependency>
</dependencies>
```

[fluo-api]: https://fluo.apache.org/apidocs/fluo/
