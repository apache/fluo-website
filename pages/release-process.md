---
layout: page
title: Release Process
permalink: /release-process/
---

### Initial Setup

Before you can release Fluo or Fluo Recipes, you will need a GPG key. For information on generating
a key look at this [ASF GPG page](https://www.apache.org/dev/openpgp.html).  After generating a key,
add it to the [KEYS] file.  The [KEYS] files contains instructions for adding to itself.  Use the 
following command to checkout the svn repository that contains the KEYS files.  Updates to this
repository will eventually sync to the website.

```bash
svn co https://dist.apache.org/repos/dist/release/fluo/
```

The maven release plugin will need credentials to stage artifacts.  You can provide the credentials
by adding the following to your `~/.m2/settings.xml` file.  Maven offers documentation about [securing
your credentials](https://maven.apache.org/guides/mini/guide-encryption.html).

```xml
<servers>
  <server>
    <!-- Project using the Apache parent pom use following ID -->
    <id>apache.releases.https</id>
    <username>your-apache-id</username>
    <password>your-apache-password</password>
  </server>
</servers>
```

### Release Fluo

Before starting the release process below, the following tasks should be complete:

 * Ensure the NOTICE file has the correct year.
 * Create release notes for project website using GitHub issues.
 * Perform testing and document results.
 * Start a gpg-agent to cache your gpg key to avoid entering your passphrase multiple times.  How
   you start this depends on your environment.  The following command works in some environments. 
   Ensure gpg-agent is configured with a sufficiently long timeout so that the cached passphrase 
   do not expire during the build.

   ```shell
   gpg-agent --daemon --use-standard-socket
   ```

Next, repeat the steps below until a good release candidate (RC) is found.  The script in
`contrib/create-release-candidate.sh` automates this process.  However there is no guarantee that it
works correctly.  Before using the script ensure you understand the process and inspect the script.
In the following steps `RCV` is short for release candidate version.  For the case where you want to
make an initial release candidate available for evaluation, but nor for voting, consider using `0`
for `RCV`.

 1. Branch main (or the current snapshot) and call the branch `<releaseVersion>-rc<RCV>-next`

 2. Prepare the release which will verify that all tests pass: `mvn release:prepare`

 3. Perform the release: `mvn release:perform`
    * This step will create a staging repository at https://repository.apache.org
    * When `release:perform` finishes, login and close the staging repository to make the artifacts available 
      for download at `https://repository.apache.org/content/repositories/orgapachefluo-REPO_ID`
    * Its very important to only close the staging repository and not release or promote it at this point.  Releasing publishes
      the artifacts to Maven central and this can not be undone.  Releasing is done after a successful vote.
    * When closing, add a comment like `Apache Fluo 1.2.0-rc3`

 4. Delete the tag created by `mvn release:pepare`.  This tag should not be pushed to Apache until
    the vote passes.  Also, a signed tag should be created instead of the one created by Maven.  So out
    of an abundance of caution its best to delete it now and create the signed tag after the vote
    passes.

    ```shell
    git tag -d rel/fluo-<releaseVersion>
    ```

 5. Push the `<releaseVersion>-rc<RCV>-next` to apache.

    ```shell
    git checkout <releaseVersion>-rc<RCV>-next
    git push apache-remote <releaseVersion>-rc<RCV>-next
    ```

 6. Create the release candidate branch `<releaseVersion>-rc<RCV>` and push it.  This branch should
    be one commit behind `<releaseVersion>-rc<RCV>-next` and one commit ahead of the branch point.

    ```shell
    git checkout -b <releaseVersion>-rc<RCV> <releaseVersion>-rc<RCV>-next~1
    git push -u apache-remote <releaseVersion>-rc<RCV>
    ```

 7. Send a message to the devs to let them know a release is staged. This [example][example-email]
    for the Fluo 1.0.0 release can be used as template.  The script
    `contrib/create-release-candidate.sh` can be used to generate this email.

When the vote passes on a release candidate, follow the steps below to complete the release using the chosen RC:

 1. Merge your RC branch into the correct branch and push those commits upstream.  The example below
    assume `main` is the correct branch.  Afterwards, you can delete your RC branch.

    ```shell
    git checkout main
    git merge <releaseVersion>-rc<RCV>-next
    git push apache-remote main
    ```

 2. Release the artifacts at https://repository.apache.org so that they get published in Maven
    Central.  You can drop any staging repos for RCs that were not chosen.  Add a comment like `Vote
    failed for Apache Fluo 1.1.0-rc3` when dropping or `Apache Fluo 1.1.0` when releasing. 

 3. Create a signed tag for the release from the chosen RC tag and push to upstream repo:

    ```shell
    # This step is optional.  Some systems that have gpg and gpg2 may not function correctly.
    # See https://bugzilla.redhat.com/show_bug.cgi?id=568406
    git config --global --get gpg.program || git config --global --add gpg.program gpg2
    ```

    ```shell
    # Create signed tag.
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
 6.  View the [website README] for instructions on how to generate Javadocs and documentation using
     the released tag.  Submit PR to the website repo to publish.

 7.  Place the source and binary tarballs in the svn distribution repo under `fluo/<releaseVersion>`.
     This is the same svn repo mentioned earlier for the KEYS file.  Follow the [ASF guidance][sigs] for
     hashes and signatures.  This step publishes the files to the ASF mirrors.

 8.  Send an email to `dev@fluo.apache.org` announcing new release.

### Test a Fluo release

#### Set up environment for all tests

1. Set the release version, ID for staging repo, and alias to configure Maven with temporary settings:
   ```shell
   export RC_VERSION=1.2.0
   export RC_STAGING=1023
   alias mvn='mvn -s /tmp/fluo-rc-maven.xml'
   ```
1. Create temporary Maven settings
   ```shell
   $ cat <<EOF >/tmp/fluo-rc-maven.xml
   <settings>
     <profiles>
       <profile>
         <id>fluoRC</id>
         <repositories>
           <repository>
             <id>fluorc</id>
             <name>fluorc</name>
             <url>https://repository.apache.org/content/repositories/orgapachefluo-\${env.RC_STAGING}/</url>
           </repository>
         </repositories>
         <pluginRepositories>
           <pluginRepository>
             <id>fluorcp</id>
             <name>fluorcp</name>
             <url>https://repository.apache.org/content/repositories/orgapachefluo-\${env.RC_STAGING}/</url>
           </pluginRepository>
         </pluginRepositories>
       </profile>
     </profiles>
     <activeProfiles>
       <activeProfile>fluoRC</activeProfile>
     </activeProfiles>
   </settings>
   EOF
   ```
1. If a new release candidate is made, update your staging repo ID.
   ```shell
   $ export RC_STAGING=1024
   ```

#### Run the integration tests of projects that use Fluo

1. Clone the [Fluo Recipes] project:
    ```shell
    $ git clone https://github.com/apache/fluo-recipes.git
    ```
1. Run the integration test
    ```shell
    $ mvn clean verify -Dfluo.version=$RC_VERSION
    ```
Below are more projects with integration tests which can be found at - `https://github.com/apache/fluo-examples.git`:
* [Phrasecount] 
* [Stresso]
* [Webindex] 


#### Setup Uno to run Fluo example applications

1. Clone [Uno] and fetch Fluo dependencies
   ```shell
   git clone https://github.com/apache/fluo-uno.git
   cd uno
   ./bin/uno fetch fluo
   ```
1. Download release tarball
   ```shell
   wget -P downloads/ https://repository.apache.org/content/repositories/orgapachefluo-${RC_STAGING}/org/apache/fluo/fluo/${RC_VERSION}/fluo-${RC_VERSION}-bin.tar.gz
   ```
1. Set `FLUO_VERSION` and `FLUO_HASH` in `conf/uno.conf`.
   ```shell
   sed -i "s/export FLUO_VERSION=[^ ]*/export FLUO_VERSION=$RC_VERSION/" conf/uno.conf
   sed -i "s/export FLUO_HASH=[^ ]*/export FLUO_HASH=$(shasum -a 256 downloads/fluo-${RC_VERSION}-bin.tar.gz | cut -d ' ' -f 1)/" conf/uno.conf
   ```
1. Set up Fluo and your shell
   ```shell
   ./bin/uno setup fluo
   eval "$(./bin/uno env)"
   ```

#### Run phrasecount example

1. Clone project
   ```shell
   git clone https://github.com/apache/fluo-examples.git
   cd phrasecount
   ```
1. Create sample data
   ```shell
   mkdir data
   cp README.md data/README.txt
   ```
1. Run phrasecount
   ```shell
   ./bin/run.sh data/
   ```

[Fluo Recipes]: https://github.com/apache/fluo-recipes
[Uno]:https://github.com/apache/fluo-uno
[Webindex]: https://github.com/apache/fluo-examples/tree/main/webindex
[Stresso]: https://github.com/apache/fluo-examples/tree/main/stresso
[Phrasecount]: https://github.com/apache/fluo-examples/tree/main/phrasecount
[website README]: https://github.com/apache/fluo-website/blob/main/README.md
[example-email]: https://lists.apache.org/thread.html/8b6ec5f17e277ed2d01e8df61eb1f1f42266cd30b9e114cb431c1c17@%3Cdev.fluo.apache.org%3E
[KEYS]: https://www.apache.org/dist/fluo/KEYS
[sigs]: https://www.apache.org/dev/release-distribution.html#sigs-and-sums
