Fluo website
============

Code powering the Fluo project website ([http://fluo.io](http://fluo.io)).

Contributions
-------------

Contributions to the website can be made by submitting pull requests to this repo. 
If you want to view your changes in your browser before submitting a pull request, 
you will need install [Jekyll] on your machine by following these [instructions].
You will also need to install all gems in the [Gemfile].

Once Jekyll is installed, use the following command to run the development server:

    jekyll serve --watch

Next, open a web browser to [http://localhost:4000](http://localhost:4000).

Fluo releases
-------------

Below are the steps required to update the Fluo project website for a new release 
(substitute `1.0.0-beta-1` with the version of your release):

1. Run the commands below to copy and convert documentation in your release tag of
   your Fluo repo to this repo:

    ```bash
    cd fluo-io.github.io
    mkdir -p docs/1.0.0-beta-1
    ./_scripts/convert-docs.py /path/to/fluo/docs/ /path/to/fluo-io.github.io/docs/fluo/1.0.0-beta-1/
    ```

2. Modify `docs/index.md` to point to new release and update the `latest_fluo_release` 
   variable in `_config.yml`.

3. Run this command to generate Javadocs from your your Fluo release tag repo and 
   copy them to this repo.  The command assumes that you have a tag in your Fluo
   repo named after your release version (i.e 1.0.0-beta-1):

    ```bash
    ./_scripts/gen-javadoc.sh 1.0.0-beta-1 /path/to/repo/fluo/modules/api /path/to/fluo-io.github.io/apidocs/fluo
    ```

4. Modify `apidocs/index.md` to point to the new javadocs that you just generated.

5. Create a blog post announcing the release in `_posts/blog/`

Fluo Recipes releases
---------------------

Steps to update website for new Fluo Recipes release:

1. Run the commands below to copy and convert documentation in your release tag.

    ```bash
    cd fluo-io.github.io
    mkdir -p docs/1.0.0-beta-1
    ./_scripts/convert-recipes.py /path/to/fluo-recipes/docs/ /path/to/fluo-io.github.io/docs/fluo-recipes/1.0.0-beta-1/
    ```

2. Modify `docs/index.md` to point to new release and update the `latest_recipes_release` variable in `_config.yml`.

3. Run this command to generate Javadocs from your Fluo release tag repo and 
   copy them to this repo.  The command assumes that you have a tag in your Fluo
   repo named after your release version (i.e 1.0.0-beta-1):

    ```bash
    ./_scripts/gen-javadoc.sh 1.0.0-beta-1 /path/to/repo/fluo-recipes /path/to/fluo-io.github.io/apidocs/fluo-recipes
    ```

4. Modify `apidocs/index.md` to point to the new javadocs that you just generated.

[Jekyll]: http://jekyllrb.com/
[Gemfile]: Gemfile
[instructions]: http://jekyllrb.com/docs/installation/
