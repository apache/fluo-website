---
layout: page
title: How To Contribute
permalink: /how-to-contribute/
---

Contributions are welcome to all Apache Fluo repositories.  All repositories follow a
[review-then-commit][rtc] process.  Prior to commit all contributions must pass any integration
tests and be approved by at least one other committer. Code reviews are done by commenting on a
GitHub pull request. If you would like to contribute, but are not sure where to start then
[contact us][cu] and/or look at issues marked [helpwanted]. Fluo committers will follow the
[Apache Code of Conduct][acc] when corresponding with a contributor. We respectfully ask all
contributors to follow this code of conduct also.

### Repositories

Contributions can be made to the following repositories.  This page contains general instructions
for all repositories.  Each repository also has a `CONTRIBUTING.md` file containing instructions
specifically for it. For the links columns below, `I` is for issues and `C` is for CONTRIBUTING.md. 

| Repository        | Links           | Description
| ----------------- | --------------- | -----------
| [Fluo][f]         | [I][fi] [C][fc] | Core Project
| [Fluo Recipes][r] | [I][ri] [C][rc] | Recipes that build on core.  Code for interoperating with other projects.
| [Website][w]      | [I][wi] [C][wc] | Source for this website.
| [Fluo Yarn][y]    | [I][yi] [C][yc] | Enables launching Fluo using YARN.
| [Fluo Docker][d]  | [I][di] [C][dc] | Support for running Fluo in Docker.  Enables launching Fluo in Mesos and Kubernetes.
| [Fluo Bytes][b]   | [I][bi] [C][bc] | An immutable Byte wrapper for Java suitable for use in APIs. 
| [Fluo Uno][u]     | [I][ui]         | Uno automates setting up Apache Accumulo or Apache Fluo (and their dependencies) on a single machine.
| [Fluo Muchos][m]  | [I][mi]         | Muchos automates setting up Apache Accumulo or Apache Fluo (and their dependencies) on a cluster.
| [Fluo Examples][e]| [I][ei]         | Collection of example projects that utilizes Apache Fluo.

### Contribution workflow

1. [Fork] and [clone] the repository you want to contribute to.
1. If needed, create an issue that describes the work.
1. Create a branch in the local clone of your fork. An example branch name is `fluo-301` which describes the repo and issue number.

   ```shell
   git checkout -b fluo-301
   ```

1. Do work and commit to your branch.
1. Ensure you works satisfies the guidelines laid out in the `CONTRIBUTING.md` file.
1. If needed, squash to the minimum number of commits. For help on squashing commits, see this [tutorial] or [StackOverflow answer][stackoverflow].
1. [Push] your branch to your fork.

   ```shell
   # Push work in local branch fluo-301 to fork
   git push origin fluo-301
   ```

1. Create a [Pull Request] in the appropriate repository.  If the work is not complete and the Pull Request is for feedback, please put `[WIP]` in the subject.
1. At least one committer (and others in the community) will review your pull request and add any comments to your code.
1. Push any changes from the review to the branch as new commits so the reviewer only needs to review new changes.  Please avoid squashing commits after the review starts.  Squashing makes it hard for the reviewer to follow the changes.
1. Repeat this process until a reviewer approves the pull request.
1. When the review process is finished, all commits on the pull request may be squashed by a committer.  Please avoid squashing as it makes it difficult for the committer to know if they are merging what was reviewed.

### Coding guidelines

All Fluo projects have configured Maven to do automatic code formatting and import organizing.  So in projects with `pom.xml` files, running `mvn compile` should format all modified code.  Please run this before committing.  The instructions below explain how to set this formatting up in your IDE.

To properly organize imports, make sure your imports look like the block below:

```
java.
javax.
<blank line>
<all other non-static imports in alphabetical order>
<blank line>
<static imports in alphabetical order>
```

This can be configured by common IDEs:

* Eclipse: ```Window -> Preferences -> Java -> Code Style -> Organize Imports```
* Intelli-J: ```Preferences -> Code Style -> Java -> Imports```

To properly format code in Eclipse :

* Go to ```Window -> Preferences -> Java -> Code Style -> Formatter```
* Click Import and import ```<local Fluo source dir>/contrib/fluo-eclipse-style.xml```
* Either configure all projects in eclipse to use this style or just the Fluo projects.

[f]: https://github.com/apache/fluo
[r]: https://github.com/apache/fluo-recipes
[w]: https://github.com/apache/fluo-website
[y]: https://github.com/apache/fluo-yarn
[d]: https://github.com/apache/fluo-docker
[b]: https://github.com/apache/fluo-bytes
[u]: https://github.com/apache/fluo-uno
[m]: https://github.com/apache/fluo-muchos
[e]: https://github.com/apache/fluo-examples
[fi]: https://github.com/apache/fluo/issues
[ri]: https://github.com/apache/fluo-recipes/issues
[wi]: https://github.com/apache/fluo-website/issues
[yi]: https://github.com/apache/fluo-yarn/issues
[di]: https://github.com/apache/fluo-docker/issues
[bi]: https://github.com/apache/fluo-bytes/issues
[ui]: https://github.com/apache/fluo-uno/issues
[mi]: https://github.com/apache/fluo-muchos/issues
[ei]: https://github.com/apache/fluo-examples/issues
[fc]: https://github.com/apache/fluo/blob/master/CONTRIBUTING.md
[rc]: https://github.com/apache/fluo-recipes/blob/master/CONTRIBUTING.md
[wc]: https://github.com/apache/fluo-website/blob/gh-pages/CONTRIBUTING.md
[yc]: https://github.com/apache/fluo-yarn/blob/master/CONTRIBUTING.md
[dc]: https://github.com/apache/fluo-docker/blob/master/CONTRIBUTING.md
[bc]: https://github.com/apache/fluo-bytes/blob/master/CONTRIBUTING.md
[tutorial]: http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html
[stackoverflow]: https://stackoverflow.com/questions/5189560/squash-my-last-x-commits-together-using-git
[rtc]: https://www.apache.org/foundation/glossary.html#ReviewThenCommit
[acc]: https://www.apache.org/foundation/policies/conduct.html
[helpwanted]: https://github.com/search?q=repo%3Aapache%2Ffluo+repo%3Aapache%2Ffluo-recipes+repo%3Aapache%2Ffluo-bytes+repo%3Aapache%2Ffluo-website+repo%3Aapache%2Ffluo-yarn+repo%3Aapache%2Ffluo-docker+repo%3Aapache%2Ffluo-uno+repo%3Aapache%2Ffluo-muchos+repo%3Aapache%2Ffluo-examples+label%3A%22help+wanted%22+type%3Aissue+state%3Aopen&type=Issues
[cu]: /contactus/
[Fork]: https://help.github.com/articles/fork-a-repo/
[Pull Request]: https://help.github.com/articles/about-pull-requests/
[Push]: https://help.github.com/articles/pushing-to-a-remote/
[clone]: https://help.github.com/articles/cloning-a-repository/
