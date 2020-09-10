# Apache Fluo website

Code powering the Apache Fluo website ([https://fluo.apache.org][production]).
[Contributing](CONTRIBUTING.md) describes how to test locally.

## Update website for new release

Below are the steps required to update the Fluo project website for a new release
of Fluo or Fluo Recipes.  The steps below assume you are releasing Fluo 1.2.0. For
a Fluo Recipes release, replace any reference to `fluo` with `recipes`.

1. Confirm that Javadocs for the release are hosted externally

2. Modify `_config.yml` for the new release:

    * Set `latest_fluo_release` to `1.2.0`
    * Verify default values (i.e Javadoc & GitHub URLs) set for `fluo-1-2` collection

3. Remove the "Future release" warning from the Fluo docs layout in `_layouts/fluo-1.2.html`

4. Add link to 1.2 documentation in `docs/index.md`.

5. Add link to 1.2 javadocs in `pages/api.md`.

6. If a post exists for the release in `_posts/release`, update the date and remove `draft: true`
   from the post to publish it.  Otherwise, create a post with release notes and resources to announce
   the release.

## Create documentation for next release

Below are steps to create documentation for the next release of Fluo or Fluo Recipes. The
directions below are for creating Fluo 1.3 docs from 1.2 docs.  For Fluo Recipes documentation,
replace any reference to `fluo` with `recipes`.

1. Create the Fluo 1.3 docs from the 1.2 docs

        cp -r _fluo-1-2 _fluo-1-3

2. Create a `fluo-1.3.html` layout and update any collection references in it to `fluo-1-3`.
   You should also add a warning banner to notify users that it's for a future release.

        cp _layouts/fluo-1.2.html _layouts/fluo-1.3.html
        vim _layout/fluo-1.3.html

3. Update `_config.yml` by adding a `fluo-1-3` collection and setting default values for it.
   You may want to keep 1.2 values for github & javadocs until 1.3 is released.
   
## Publishing

### Automatic Staging

Changes pushed to our `main` branch will automatically trigger [Jekyll] to
build our site from that branch and push the result to our `asf-staging`
branch, where they will be served on [our default staging site][staging].

### Publishing Staging to Production

First, add our repository as a remote in your local clone, if you haven't
already done so (these commands assume the name of that remote is 'upstream').

Example:

```bash
git clone https://github.com/<yourusername>/fluo-website
cd fluo-website
git remote add upstream https://github.com/apache/fluo-website
```

Next, publish the staging site to production by updating the `asf-site` branch
to match the contents in the `asf-staging` branch:

```bash
# Step 0: stay in main branch; you never need to switch
git checkout main

# Step 1: update your upstream remote
git remote update upstream

# Step 2: push upstream/asf-staging to upstream/asf-site
# run next command with --dry-run first to see what it will do without making changes
git push upstream upstream/asf-staging:asf-site
```

A convenience script can be found that performs these steps for you, after
asking which remote you want to use. It is located in the `main` branch at
`_scripts/publish.sh`

Note that Step 2 should always be a fast-forward merge. That is, there should
never be any reason to force-push it if everything is done correctly. If extra
commits are ever added to `asf-site` that are not present in `asf-staging`,
then those branches will need to be sync'd back up in order to continue
avoiding force pushes.

The final site can be viewed [here][production].


[Jekyll]: https://jekyllrb.com/
[production]: https://fluo.apache.org
[staging]: https://fluo.staged.apache.org
