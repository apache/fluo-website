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

# Testing locally

If you want to view your changes in your browser before submitting a pull request, you will need
install all of the gems in the [Gemfile] to serve the website in your browser using [Jekyll]. This
can be done by following these instructions:

1. After you have Ruby and RubyGems installed on your machine, install [Bundler]:

        gem install bundler

2. Use [Bundler] to install all gems in the [Gemfile] of this repo.

        cd fluo-website/
        bundle install

3. Run the following command to have Jekyll serve the website locally:

        bundle exec jekyll serve --watch

4. Open your web browser to [http://localhost:4000](http://localhost:4000).

[contribute]: https://fluo.apache.org/how-to-contribute/
[Jekyll]: http://jekyllrb.com/
[Bundler]: http://bundler.io/
[Gemfile]: Gemfile

