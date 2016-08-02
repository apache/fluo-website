---
layout: page
title: Release Process
permalink: /release-process/
---

<div class="alert alert-danger" role="alert">Please note - These instructions are for releasing Fluo before it became an ASF project.  After the first Apache release, they will be updated to reflect how to release Apache Fluo on ASF infrastructure</div>

### Initial Setup

Before you can release Fluo or Fluo Recipes, you will need to set up a GPG client, create a [sonatype account], and have another Fluo committer request to give you deployment access for the Fluo project on sonatype.  Once you have a sonatype account, you should add your account details to your Maven settings.xml in the following format:

```xml
<servers>
  <server>
    <id>sonatype-nexus-staging</id>
    <username>USER</username>
    <password>PASS</password>
  </server>
  <server>
    <id>sonatype-nexus-snapshots</id>
    <username>USER</username>
    <password>PASS</password>
  </server>
</servers>
```

See this [documentation] for more information on setting up your environment.

### Release Fluo

Before starting the release process below, the following tasks should be complete:
 
 * Create release notes for project website using GitHub issues.
 * Perform testing and document results
 * Start a gpg-agent to cache your gpg key to avoid entering your passphrase multiple times.

   ```shell
   gpg-agent --daemon --use-standard-socket
   ```

Next, repeat the steps below until a good release candidate (RC) is found:

 1. Branch master (or the current snapshot) and call the branch `<releaseVersion>-RC`

 2. Except in Maven POMs (which will be updated by the next step), change any version references in docs and code from `<releaseVersion>-SNAPSHOT` to `<releaseVersion>`.  Commit changes to branch.

 3. Run integration tests using `mvn clean verify`

 4. Prepare the release which will verify that all tests pass: `mvn release:prepare`

 5. Perform the release: `mvn release:perform`
    * This step will create a staging repository viewable only to you when login to https://oss.sonatype.org/#stagingRepositories
    * When `release:perform` finishes, you will need to close the staging repository to make it viewable to anyone at https://oss.sonatype.org/content/repositories/iofluo-REPO_ID

 6. Create an RC tag (i.e `<version#>-<rc#>`) from the tag created by the release plugin (a branch could work instead of a tag but the point is to remove the release tag because the codebase has not been released yet). This new branch/tag should have the non-snapshot version in the poms.  The RC tag can be pushed to a fork for others to view.

    ```shell
    # Creates 1.0.0-beta-1-RC1 from 1.0.0-beta-1 
    git tag 1.0.0-beta-1-RC1 1.0.0-beta-1
    # Delete 1.0.0-beta-1
    git tag -d 1.0.0-beta-1
    # Push RC tag to fork
    git push origin 1.0.0-beta-1-RC1
    ```

 7. The artifacts will be staged in nexus OSS. Send a message to the devs to let them know a release is staged. 

 8. Give enough time (Apache recommends 72 hours) for everyone to check out the distribution tarball from Sonatype OSS and verify signatures, hashes, functional tests, etc... Sonatype OSS does have it's own validation of the artifacts which includes verifying a valid GPG signature, though I do not believe it verifies that it belonged to a trusted committer so that'll need to be done by other committers.

When consensus has been reached on a release candidate, follow the steps below to complete the release using the chosen RC:

 1. Merge your RC branch into master and push those commits upstream.  Afterwards, you can delete your RC branch.

    ```shell
    git checkout master
    git merge 1.0.0-beta-RC
    git push upstream master
    git branch -d 1.0-0-beta-RC
    ```

 2. [Release the artifacts] in Sonatype OSS so that they get published in Maven Central.  You can drop any staging repos for RCs that were not chosen. 

 3. Create a signed tag for the release from the chosen RC tag and push to upstream repo:

    ```shell
    # Create signed tag from RC2 tag.
    # You may need to use -u <key-id> to specify GPG key
    git tag -s 1.0.0-beta-1 1.0.0-beta-1-RC2
    # Push signed tag to upstream repo
    git push upstream 1.0.0-beta-1
    ```

 4. Attach Fluo tarball to GitHub release page.

 5. Remove all RC tags

    ```shell
    # Remove tag locally
    git tag -d 1.0.0-beta-1-RC1
    # Remove tag on fork
    git push --delete origin 1.0.0-beta-1-RC1
    ```
 6.  View the [website README] for instructions on how to generate Javadocs and documentation using the released tag.  Submit PR to the website repo to publish.
 
 7.  Send an email to `dev@fluo.incubator.apache.org` announcing new release.

[website README]: https://github.com/apache/incubator-fluo-website/blob/master/README.md
[documentation]: http://central.sonatype.org/pages/apache-maven.html
[sonatype account]: https://issues.sonatype.org/
[Release the artifacts]: http://central.sonatype.org/pages/releasing-the-deployment.html
