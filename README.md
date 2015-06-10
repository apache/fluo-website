Fluo website
============

The Fluo website is powered by [Jekyll][1].

Before you can run the website locally, you will need to [install][2] Jekyll.  

Once Jekyll is installed, use the following command to run the website locally:
```
jekyll serve --watch

```
Then, browse to `http://localhost:4000`.

Generating Javadocs
-------------------

For each release, Javadocs need to be generated for the Fluo codebase and copied to the `apidocs/` directory.

This process is scripted by `gen-javadocs.sh` which is run with the release version and the path to your Fluo repo:

```
./_scripts/gen-javadoc.sh 1.0.0-beta-1 /path/to/repo/fluo
```

After running `gen-javadoc.sh`, you will need to modify the API index at `apidocs/index.md` to include the javadocs 
for the new release.

[1]: http://jekyllrb.com/
[2]: http://jekyllrb.com/docs/installation/
