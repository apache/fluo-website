---
title: Scanning Code
---


```java
  private static void exercise(MiniFluo mini, FluoClient client) {
    Column fName = new Column("name", "first");
    Column lName = new Column("name", "last");
    Column bravery = new Column("attr","bravery");

    try(Transaction tx1 = client.newTransaction()) {
      tx1.set("kerbalnaut0001", fName, "Jebediah");
      tx1.set("kerbalnaut0001", lName, "Kerman");
      tx1.set("kerbalnaut0001", bravery, "5");

      tx1.set("kerbalnaut0002", fName, "Bill");
      tx1.set("kerbalnaut0002", lName, "Kerman");
      tx1.set("kerbalnaut0002", bravery, "2");

      tx1.set("kerbalnaut0003", fName, "Bob");
      tx1.set("kerbalnaut0003", lName, "Kerman");
      tx1.set("kerbalnaut0003", bravery, "1");

      tx1.set("bravery5", new Column("id", "kerbalnaut0001"), "5");
      tx1.set("bravery2", new Column("id", "kerbalnaut0002"), "2");
      tx1.set("bravery1", new Column("id", "kerbalnaut0003"), "1");

      tx1.commit();
    }

    try(Snapshot s1 = client.newSnapshot()) {
       //scan over an entire row
       CellScanner cellScanner = s1.scanner().over(Span.exact("kerbalnaut0002")).build();
       System.out.println("Scan 1 :");
       for (RowColumnValue rcv : cellScanner) {
         System.out.println("\t"+rcv);
       }

       //scan over a row and column family
       cellScanner = s1.scanner().over(Span.exact("kerbalnaut0002", new Column("name"))).build();
       System.out.println("\nScan 2 :");
       for (RowColumnValue rcv : cellScanner) {
         System.out.println("\t"+rcv);
       }

       //scan over two columns
       cellScanner = s1.scanner().over(Span.prefix("kerbalnaut")).fetch(fName, bravery).build();
       System.out.println("\nScan 3 :");
       //use Java lambda's to print instead of foreach loop
       cellScanner.forEach(rcv -> System.out.println("\t"+rcv));
    }
  }
```

The code above prints :

```
Starting MiniFluo ... started.
Scan 1 :
	kerbalnaut0002 attr bravery  2
	kerbalnaut0002 name first  Bill
	kerbalnaut0002 name last  Kerman

Scan 2 :
	kerbalnaut0002 name first  Bill
	kerbalnaut0002 name last  Kerman

Scan 3 :
	kerbalnaut0001 attr bravery  5
	kerbalnaut0001 name first  Jebediah
	kerbalnaut0002 attr bravery  2
	kerbalnaut0002 name first  Bill
	kerbalnaut0003 attr bravery  1
	kerbalnaut0003 name first  Bob
```
