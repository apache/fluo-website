<!--
  Licensed to the Apache Software Foundation (ASF) under one
  or more contributor license agreements.  See the NOTICE file
  distributed with this work for additional information
  regarding copyright ownership.  The ASF licenses this file
  to you under the Apache License, Version 2.0 (the
  "License"); you may not use this file except in compliance
  with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing,
  software distributed under the License is distributed on an
  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  KIND, either express or implied.  See the License for the
  specific language governing permissions and limitations
  under the License.
-->

# Apache Fluo website

[![Build Status][ti]][tl] [![Apache License][li]][ll]

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

Changes pushed to our `main` branch will automatically trigger [Jekyll] to
build our site from that branch and push the result to our `asf-site`
branch, where they will be served on [our production site][production].

## Testing using Docker environment 

A containerized development environment can be built using the local
Dockerfile. You can build it with the following command:

```bash
docker build -t fluo-site-dev .
```

This action will produce a `fluo-site-dev` image, with all the website's build
prerequisites preinstalled. When a container is run from this image, it
will perform a `jekyll serve` command with the polling option enabled,
so that changes you make locally will be immediately reflected after
reloading the page in your browser.

When you run a container using the `fluo-site-dev` image, your current working
directory will be mounted, so that any changes made by the build inside
the container will be reflected in your local workspace. This is done with
the `-v` flag. To run the container, execute the following command:

```bash
docker run -it -v "$PWD":/mnt/workdir -p 4000:4000 fluo-site-dev
```

While this container is running, you will be able to review the rendered website
in your local browser at the address printed in the shell ([http://0.0.0.0:4000/](http://0.0.0.0:4000/)).

Appending `/bin/bash` to the end of the docker command above will provide shell access. This is useful for adding new 
gems, or modifying the Gemfile.lock for updating existing dependencies.
When using shell access, the local directory must be mounted to ensure
the Gemfile and Gemfile.lock updates are reflected in your local
environment so you can create a commit and submit a PR.

You may need to manually delete the `_site` or `.jekyll-cache` directories if
they already exist and are causing issues with the build.

[Jekyll]: https://jekyllrb.com/
[production]: https://fluo.apache.org
[ti]: https://github.com/apache/fluo-website/workflows/CI/badge.svg
[tl]: https://github.com/apache/fluo-website/actions
[li]: http://img.shields.io/badge/license-ASL-blue.svg
[ll]: https://github.com/apache/fluo-website/blob/main/LICENSE
