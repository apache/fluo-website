# Apache Fluo website

Code powering the Apache Fluo website ([https://fluo.apache.org](https://fluo.apache.org)).

## Contributions

Contributions to the website can be made by submitting pull requests to this repo.

If you want to view your changes in your browser before submitting a pull request, 
you will need install all of the gems in the [Gemfile] to serve the website in your
browser using [Jekyll]. This can be done by following these instructions:

1. After you have Ruby and RubyGems installed on your machine, install [Bundler]:

        gem install bundler

2. Use [Bundler] to install all gems in the [Gemfile] of this repo.

        cd incubator-fluo-website/
        bundle install

3. Run the following command to have Jekyll serve the website locally:

        bundle exec jekyll serve --watch

4. Open your web browser to [http://localhost:4000](http://localhost:4000).

## Apache Fluo releases

Below are the steps required to update the Fluo project website for a new release 
(substitute `1.0.0-beta-1` with the version of your release):

1. Run the commands below to copy and convert documentation in your release tag of
   your Fluo repo to this repo:

    ```bash
    cd fluo-website/
    mkdir -p docs/1.0.0-beta-1
    ./_scripts/convert-docs.py /path/to/fluo/docs/ /path/to/fluo-website/docs/fluo/1.0.0-beta-1/
    ```

2. Modify `docs/index.md` to point to new release and update the `latest_fluo_release` 
   variable in `_config.yml`.

3. Run this command to generate Javadocs from your your Fluo release tag repo and 
   copy them to this repo.  The command assumes that you have a tag in your Fluo
   repo named after your release version (i.e 1.0.0-beta-1):

    ```bash
    ./_scripts/gen-javadoc.sh 1.0.0-beta-1 /path/to/repo/fluo/modules/api /path/to/fluo-website/apidocs/fluo
    ```

4. Modify `apidocs/index.md` to point to the new javadocs that you just generated.

5. Create a blog post announcing the release in `_posts/blog/`

## Apache Fluo Recipes releases

Steps to update website for new Fluo Recipes release:

1. Run the commands below to copy and convert documentation in your release tag.

    ```bash
    cd fluo-website
    mkdir -p docs/1.0.0-beta-1
    ./_scripts/convert-recipes.py /path/to/fluo-recipes/docs/ /path/to/fluo-website/docs/fluo-recipes/1.0.0-beta-1/
    ```

2. Modify `docs/index.md` to point to new release and update the `latest_recipes_release` variable in `_config.yml`.

3. Run this command to generate Javadocs from your Fluo release tag repo and 
   copy them to this repo.  The command assumes that you have a tag in your Fluo
   repo named after your release version (i.e 1.0.0-beta-1):

    ```bash
    ./_scripts/gen-javadoc.sh 1.0.0-beta-1 /path/to/repo/fluo-recipes /path/to/fluo-website/apidocs/fluo-recipes
    ```

4. Modify `apidocs/index.md` to point to the new javadocs that you just generated.

[Jekyll]: http://jekyllrb.com/
[Bundler]: http://bundler.io/
[Gemfile]: Gemfile
[instructions]: http://jekyllrb.com/docs/installation/
