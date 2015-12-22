Fluo website
============

Code powering the Fluo project website ([http://fluo.io](http://fluo.io)).

Contributions
-------------

Contributions to the website can be made by submitting pull requests to this repo. 
If you want to view your changes in your browser before submitting a pull request, 
you will need install [Jekyll] on your machine by following these [instructions].
In addition to Jekyll, install redcarpet to format markdown.

    gem install redcarpet

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
    ./_scripts/convert-docs.py /path/to/fluo/docs/ /path/to/fluo-io.github.io/docs/1.0.0-beta-1/
    ```

2. Run this command to generate Javadocs from your your Fluo release tag repo and 
   copy them to this repo.  The command assumes that you have a tag in your Fluo
   repo named after your release version (i.e 1.0.0-beta-1):

    ```bash
    ./_scripts/gen-javadoc.sh 1.0.0-beta-1 /path/to/repo/fluo
    ```

3. Modify `apidocs/index.md` to point to the new javadocs that you just generated.

4. Create a blog post announcing the release in `_posts/blog/`

[Jekyll]: http://jekyllrb.com/
[instructions]: http://jekyllrb.com/docs/installation/
