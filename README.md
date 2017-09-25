# Apache Fluo website

Code powering the Apache Fluo website ([https://fluo.apache.org](https://fluo.apache.org)).
[Contributing](CONTRIBUTING.md) instruction decribe how to test locally.

## Apache Fluo releases

Below are the steps required to update the Fluo project website for a new release 
(substitute `1.0.0-beta-1` with the version of your release):

1. Run the commands below to copy and convert documentation in your release tag of
   your Fluo repo to this repo:

    ```bash
    cd fluo-website/
    mkdir -p docs/fluo/1.0.0-beta-1
    ./_scripts/convert-fluo-docs.py /path/to/fluo/docs/ /path/to/fluo-website/docs/fluo/1.0.0-beta-1/
    ```

2. Modify `docs/index.md` to point to new release and update the `latest_fluo_release` 
   variable in `_config.yml`.

3. Confirm that javadocs are hosted externally and modify `pages/api.md` to point to link to them.

4. Create a post in `_posts/release` with release notes and resources to announce release.

## Apache Fluo Recipes releases

Steps to update website for new Fluo Recipes release:

1. Run the commands below to copy and convert documentation in your release tag.

    ```bash
    cd fluo-website
    mkdir -p docs/fluo-recipes/1.0.0-beta-1
    ./_scripts/convert-recipes-docs.py /path/to/fluo-recipes/docs/ /path/to/fluo-website/docs/fluo-recipes/1.0.0-beta-1/
    ```

2. Modify `docs/index.md` to point to new release and update the `latest_recipes_release` variable in `_config.yml`.

3. Confirm that javadocs are hosted externally and modify `pages/api.md` to point to link to them.

4. Create a post in `_posts/release` with release notes and resources to announce release.

[instructions]: http://jekyllrb.com/docs/installation/
