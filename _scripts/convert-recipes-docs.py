#!/usr/bin/python

import sys
from os import listdir, makedirs
from os.path import isfile, join, exists
import shutil

if len(sys.argv) != 3:
  print "Usage: ./convert-recipes.py <inputDocsDir> <outputDocsDir>"
  sys.exit(-1)

input_dir = sys.argv[1]
output_dir = sys.argv[2]

args = output_dir.rpartition("/docs")
url_prefix = args[1] + args[2]
release_ver = url_prefix.split("/")[3]
github_prefix = "https://github.com/apache/fluo-recipes/blob/{0}/modules/".format(release_ver)
javadocs_prefix = "{{ site.api_static }}/fluo-recipes-FIXME/" + release_ver + "/"

def path_to_url(path):
  if path.find("#") != -1:
    print "WARNING - URL references anchor tag #: ", path.strip()
  url = url_prefix + path.rpartition("/")[2].replace(".md", "/")
  if url.endswith("/index/"):
    return url.replace("/index/", "/")
  return url

def convert_file(inPath, outPath):

  print "Creating ", outPath

  with open(inPath) as fin:

    # skip license
    line = ''
    while not line.startswith('-->'):
      line = fin.readline().strip()

    # read title
    title = ''
    while len(title) == 0:
      title = fin.readline().strip()
    title = title.lstrip(' #').strip()

    fin.readline()

    if inPath.endswith("README.md"):
      title = "Fluo Recipes {0} Documentation".format(release_ver)

    with open(outPath, "w") as fout:
      print >> fout, "---" 
      print >> fout, "layout: recipes-doc" 
      print >> fout, "title:", title 
      print >> fout, "version:", release_ver
      print >> fout, "---"

      if inPath.endswith("README.md"):
        fin.readline()
        fin.readline()

      for line in fin:
        if line.startswith("["):
          if line.find(".md") != -1:
            for word in line.split(' '):
              if word.find(".md") != -1:
                fout.write(path_to_url(word))
              else:
                fout.write(word+" ")
          elif line.find("../modules") != -1:
            if line.strip().endswith(".java"):
              start = line.find("../modules/")
              end = line.find("apache/fluo")
              fout.write(line.replace(line[start:end], javadocs_prefix).replace(".java", ".html"))
            else:
              fout.write(line.replace("../modules/", github_prefix))
          else:
            fout.write(line)
        else:
          fout.write(line)

convert_file(join(input_dir,"../README.md"), join(output_dir, "index.md"))

for f in listdir(input_dir):
  fn = join(input_dir, f)
  if isfile(fn) and fn.endswith(".md"):
    convert_file(fn, join(output_dir, f))
