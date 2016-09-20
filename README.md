Fluo Tour
---------

This git repository provides a barebones Maven+Java environment for the [Fluo Tour][tour].  As you
go through the tour edit [Main.java] and use the following command to get all of the correct
dependencies on the classpath and execute Main.

```bash
mvn -q clean compile exec:java
```

The command takes a bit to run because it starts a MiniAccumulo and MiniFluo
each time.

[tour]: https://fluo.apache.org/tour
[Main.java]: src/main/java/ft/Main.java

