# Apache Fluo website

Code powering the Apache Fluo website ([https://fluo.apache.org](https://fluo.apache.org)).
[Contributing](CONTRIBUTING.md) decribes how to test locally.

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

Below are steps to create documentaton for the next release of Fluo or Fluo Recipes. The
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
   
## Committer instructions

To publish Fluo's website the `gh-pages` branch must be rendered into the `asf-site` 
branch.  The script `_scripts/git-hooks/post-commit` automates rendering into the `asf-site` branch.
The commands below serve as a guide for committers who wish to publish the web site.

```bash
 # ensure local asf-site branch is up to date
 git checkout asf-site 
 git pull upstream asf-site

 # switch to gh-pages branch, update it, and build new site 
 git checkout gh-pages
 git pull upstream gh-pages 
 ./_scripts/git-hooks/post-commit 

 # switch to asf-site, look at the commit created by post-commit script, and push it if ok
 git checkout asf-site 
 git log -p
 git push upstream asf-site 
```

In the commands above `upstream` is 

```
$ git remote -v | grep upstream
upstream	https://gitbox.apache.org/repos/asf/fluo-website/ (fetch)
upstream	https://gitbox.apache.org/repos/asf/fluo-website/ (push)``
```
