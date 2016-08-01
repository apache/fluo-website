---
layout: page
title: How To Contribute
permalink: /how-to-contribute/
---

Contributions are welcome to all Apache Fluo repositories ([Fluo][f], [Fluo Recipes][r]) and the [Fluo project website][w].  All repositories follow a [review-then-commit][rtc] process.
This means that all contributions must pass any integration tests and be reviewed before being committed. Code reviews are done by commenting on a GitHub pull request.

### Contribution workflow
 
1. Make sure you have a fork of the repository ([Fluo][f], [Fluo Recipes][r], [Fluo Website][w]) that you want contribute to.
1. Create an issue that describes the work.  Each Fluo repository has its own issue tracker: [Fluo][fi], [Fluo Recipes][ri], [Fluo Website][wi]
1. Create a branch in the local clone of your fork. An example branch name is `fluo-301` which describes the repo and issue number.

   ```shell
   git checkout -b fluo-301
   ```

1. Do work and commit to your branch.
1. If your branch becomes stale, rebase it to master.

   ```shell
   # checkout master
   git checkout master
   # pull latest commits from upstream
   git pull upstream master
   # checkout your branch
   git checkout fluo-301
   # rebase master to bring latest commits into your branch
   # follow any insructions to resolve conflicts
   git rebase master
   # update your branch on your fork
   git push -f origin fluo-301
   ```

1. When you are ready to create a pull request, squash to the minimum number of commits. For help on squashing commits, see this [tutorial] or [StackOverflow answer][stackoverflow].
1. Push your branch `fluo-301` to your fork

   ```shell
   # add -f to command below if you squashed commits
   # and previously pushed branch to your fork
   git push origin fluo-301
   ```
1. Create a pull request on the GitHub page of the repo (e.g. [Fluo][f], [Fluo Recipes][r], [Fluo Website][w]) that you want to contribute to.  The pull request should merge your branch (e.g. `fluo-301`) in your fork into the master branch of the repo.
1. At least one committer (and others in the community) will review your pull request and add any comments to your code.
1. Reviewers should make comments at bottom of the pull request or in "Files Changed".  Avoid commenting on commits as these comments will disappear if the branch is rebased as rebasing generates new commits for the pull request.
1. Push any changes from the review to the branch as new commits so the reviewer only needs to review new changes.
1. Repeat this process until a reviewer comments with a +1.
1. When the review process is finished, all commits on the branch of the pull request should be squashed into the minimum number of commits by the developer.  The reviewer should then merge the pull request.

### Coding guidelines

Make sure your imports look like the block below:

```
java.
javax.
<blank line>
<all other non-static imports in alphabetical order>
<blank line>
<static imports in alphabetical order>
```

This can be configured by common IDEs:

* Eclipse: ```Window -> Preferences -> Java -> Organize Imports```
* Intelli-J: ```Preferences -> Code Style -> Java -> Imports```

[f]: https://github.com/apache/fluo
[r]: https://github.com/apache/fluo-recipes
[w]: https://github.com/apache/incubator-fluo-website
[fi]: https://github.com/apache/fluo/issues
[ri]: https://github.com/apache/fluo-recipes/issues
[wi]: https://github.com/apache/incubator-fluo-website/issues
[tutorial]: http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html
[stackoverflow]: http://stackoverflow.com/questions/5189560/squash-my-last-x-commits-together-using-git
[rtc]: http://www.apache.org/foundation/glossary.html#ReviewThenCommit
