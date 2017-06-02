---
layout: page
title: Release Process
permalink: /release-process/
---

### Initial Setup

Before you can release Fluo or Fluo Recipes, you will need a GPG key. For information on generating
a key look at this [ASF GPG page](https://www.apache.org/dev/openpgp.html).  After generating a key,
add it to the [KEYS](https://www.apache.org/dist/incubator/fluo/KEYS) file.

The maven release plugin will need credentials to stage artifacts.  You can provide the credentials
by adding the following to your `~/.m2/settings.xml` file.  You may want remove your password after
running maven.

```xml
<servers>
  <server>
    <id>apache.releases.https</id>
    <username>your-apache-id</username>
    <password>your-apache-password</password>
  </server>
</servers>
```

### Release Fluo

Before starting the release process below, the following tasks should be complete:

 * Create release notes for project website using GitHub issues.
 * Perform testing and document results
 * Start a gpg-agent to cache your gpg key to avoid entering your passphrase multiple times.

   ```shell
   gpg-connect-agent reloadagent /bye
   ```

Next, repeat the steps below until a good release candidate (RC) is found.  The script in
`contrib/create-release-candidate.sh` automates this process.  However there is no guarantee that it
works correctly.  Before using the script ensure you understand the process and inspect the script.
In the following steps `RCV` is short for release candidate version.

 1. Branch master (or the current snapshot) and call the branch `<releaseVersion>-rc<RCV>-next`

 2. Except in Maven POMs (which will be updated by the next step), change any version references in docs and code from `<releaseVersion>-SNAPSHOT` to `<releaseVersion>`.  Commit changes to branch.

 3. Prepare the release which will verify that all tests pass: `mvn release:prepare`

 4. Perform the release: `mvn release:perform`
    * This step will create a staging repository viewable only to you when login to https://repository.apache.org
    * When `release:perform` finishes, you will need to close the staging repository to make it viewable to anyone at  https://repository.apache.org/content/repositories/orgapachefluo-REPO_ID

 5. Delete the tag created by Maven in previous step.  This tag should not be pushed to Apache until the vote passes.  Also, a signed tag should be created instead of the one created by Maven.  So out of an abundance of caution its best to delete it now and create the signed tag after the vote passes.

    ```shell
    git tag -D rel/fluo-<releaseVersion>
    ```

 6. Push the `<releaseVersion>-rc<RCV>-next` to apache.

    ```shell
    git checkout <releaseVersion>-rc<RCV>-next
    git push apache-remote <releaseVersion>-rc<RCV>-next
    ```

 7. Create the release candidate branch `<releaseVersion>-rc<RCV>` and push it.  This branch should be one commit behind `<releaseVersion>-rc<RCV>-next`

    ```shell
    git checkout -b <releaseVersion>-rc<RCV> <releaseVersion>-rc<RCV>-next~1
    git push -u apache-remote <releaseVersion>-rc<RCV>
    ```

 8. Send a message to the devs to let them know a release is staged. This [example][example-email] for the Fluo 1.0.0 release can be used as template.  The script `contrib/create-release-candidate.sh` can be used to generate this email.

When the vote passes on a release candidate, follow the steps below to complete the release using the chosen RC:

 1. Merge your RC branch into master and push those commits upstream.  Afterwards, you can delete your RC branch.

    ```shell
    git checkout master
    git merge <releaseVersion>-rc<RCV>-next
    git push apache-remote master
    ```

 2. Release the artifacts at https://repository.apache.org so that they get published in Maven Central.  You can drop any staging repos for RCs that were not chosen.

 3. Create a signed tag for the release from the chosen RC tag and push to upstream repo:

    ```shell
    # Create signed tag from RC2 tag.
    # You may need to use -u <key-id> to specify GPG key
    git tag  -f -m 'Apache Fluo <releaseVersion>' -s rel/fluo-<releaseVersion> <releaseVersion>-rc<RCV>
    # Verify the tag is the expected commit
    git log -1 rel/fluo-<releaseVersion>
    # Push signed tag to upstream repo
    git push apache-remote rel/fluo-<releaseVersion>
    ```

 5. Delete all RC branches.

    ```shell
    git push apache-remote --delete <releaseVersion>-rc<RCV>-next
    git branch -d <releaseVersion>-rc<RCV>-next
    git push apache-remote --delete <releaseVersion>-rc<RCV>
    git branch -d <releaseVersion>-rc<RCV>
    ```
 6.  View the [website README] for instructions on how to generate Javadocs and documentation using the released tag.  Submit PR to the website repo to publish.

 7.  Send an email to `dev@fluo.incubator.apache.org` announcing new release.

[website README]: https://github.com/apache/incubator-fluo-website/blob/master/README.md
[example-email]: https://lists.apache.org/thread.html/8b6ec5f17e277ed2d01e8df61eb1f1f42266cd30b9e114cb431c1c17@%3Cdev.fluo.apache.org%3E
