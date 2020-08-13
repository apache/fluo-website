<!--
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Contributing to Fluo Website

Contributions to the website can be made by submitting pull requests to this repo.  Checkout [How to
Contribute][contribute] on for general instructions on contributing to Fluo projects.

## Local Builds for Testing

### Setting up Your Jekyll/Bundler Environment

Ruby and RubyGems are required to use Jekyll and Bundler, so first make sure
you have those on your machine.

If you are using an OS packaged version of Ruby, you may also need to install
the ruby-dev (Ubuntu) or ruby-devel (Fedora) package as well to build any
native code for gems that are installed later. Installing these will also
ensure your system's RubyGems package is installed. Depending on your OS, you
may also need other packages to install/build gems, such as ruby-full, make,
gcc, nodejs, build-essentials, or patch.

Once Ruby, RubyGems, and any necessary native tools are installed, you are
ready to install [Bundler] to manage the remaining RubyGem dependencies.
Bundler is included in Ruby 2.6 and later as a default gem, so installing it
may not be needed.

Because we use [Bundler] to install specific versions of gems, it is not
recommended to use an OS packaged version of gems other than what comes
built-in. If you are using an OS packaged version of Ruby, it is __strongly__
recommended to avoid `sudo` when installing additional gems, in order to avoid
conflicting with your system's package-managed installation. Instead, you can
specify a `GEM_HOME` directory for installing gems locally in your home
directory. You can do this in your `$HOME/.bashrc` file or other appropriate
place for your environment:

```bash
# in .bashrc
export GEM_HOME=$HOME/.gem/ruby
```

With Ruby installed on your machine, you can install [Bundler] using the
command below:

```bash
# not necessary in Ruby >2.6, since it is a default gem since 2.6
gem install bundler
```

Next, use [Bundler] to install [Jekyll] and other dependencies needed to run
the website (this command assumes your current working directory is your clone
of this repository with the `main` branch checked out, because that's where
the Gemfile dependency list exists).

```bash
bundle install
```

### Testing with the Built-in Jekyll Webserver

The command to serve the site contents using Jekyll's built-in webserver is as
follows (this webserver may behave differently than apache.org's servers).

```bash
bundle exec jekyll serve -w
```

You do __NOT__ need to execute a `bundle exec jekyll build` command first, as
the `serve` command is sufficient to both build the site and serve its
contents. By default, it will also try to re-build any pages you change while
running the webserver, which can be quite useful if trying to get some CSS or
HTML styled "just right".

Jekyll will print a local URL where the site can be viewed (usually,
[http://0.0.0.0:4000/](http://0.0.0.0:4000/)).


[Bundler]: https://bundler.io/
[Jekyll]: https://jekyllrb.com/
[contribute]: https://fluo.apache.org/how-to-contribute/
[kramdown]: https://kramdown.gettalong.org/
[production]: https://fluo.apache.org
[staging]: https://fluo.staged.apache.org
