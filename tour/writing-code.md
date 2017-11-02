---
title: Writing and Running Fluo code
---

Following the Fluo tour will require writing code that uses Fluo's API.  There is a git repository
with a basic skeleton that will help you get started quickly.   The commands below shows how to
obtain, edit, and run this basic skeleton.

```bash
#clone branch with starter code
git clone -b fluo-tour https://gitbox.apache.org/repos/asf/fluo-website fluo-tour
cd fluo-tour

#edit Main (all of the following exercises will require this)
nano src/main/java/ft/Main.java

#using Maven, run Main (all of the following exercises will require this)
mvn -q clean compile exec:java
```

Because it is so closely related to the website, this starter code is located in a branch of Fluo's
website.  The starter project has its [own readme][readme] also.

[readme]: https://github.com/apache/fluo-website/tree/fluo-tour
