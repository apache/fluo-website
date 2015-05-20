#!/usr/bin/python

import sys
from os import listdir, makedirs
from os.path import isfile, join, exists
import shutil

if len(sys.argv) != 3:
  print "Usage: ./convert-docs.py <inputDocsDir> <outputDocsDir>"
  sys.exit(-1)

input_dir = sys.argv[1]
output_dir = sys.argv[2]

args = output_dir.rpartition("/docs")
url_prefix = args[1] + args[2]
release_ver = url_prefix.split("/")[2]
github_prefix = "https://github.com/fluo-io/fluo/blob/{0}/modules/".format(release_ver)
resources_prefix = "/docs/{0}/resources/".format(release_ver)

def path_to_url(path):
  url = url_prefix + path.rpartition("/")[2].replace(".md", "/")
  if url.endswith("/index/"):
    return url.replace("/index/", "/")
  return url

def convert_file(inPath, outPath):

  print "Creating ", outPath

  with open(inPath) as fin:
    title = fin.readline().strip()
    fin.readline()

    if inPath.endswith("README.md"):
      title = "Fluo {0} Documentation".format(release_ver)

    with open(outPath, "w") as fout:
      print >> fout, "---" 
      print >> fout, "layout: page" 
      print >> fout, "title: ", title 
      print >> fout, "permalink:", path_to_url(outPath)  
      print >> fout, "---"

      if inPath.endswith("README.md"):
        fin.readline()
        fin.readline()
        print >> fout, "\n**Please Note** - This documentation is for the latest Fluo release.  Documentation for prior releases can be found [here](/docs/)"

      for line in fin:
        if line.startswith("["):
          if line.find(".md") != -1:
            for word in line.split(' '):
              if word.strip().endswith(".md"):
                fout.write(path_to_url(word))
              else:
                fout.write(word+" ")
          elif line.find("../modules") != -1:
            fout.write(line.replace("../modules/", github_prefix))
          elif line.find("resources/") and any(x in line for x in ('.png','.jpg','.pdf')):
            fout.write(line.replace("resources/", resources_prefix))
          else:
            fout.write(line)
        else:
          fout.write(line)

convert_file(join(input_dir,"../README.md"), join(output_dir, "index.md"))

for f in listdir(input_dir):
  fn = join(input_dir, f)
  if isfile(fn) and fn.endswith(".md"):
    convert_file(fn, join(output_dir, f))

src_resources = join(input_dir, 'resources')
dst_resources = join(output_dir, 'resources')

if not exists(dst_resources):
  makedirs(dst_resources)

for f in listdir(src_resources):
  src = join(src_resources, f)
  dst = join(dst_resources, f)

  if not exists(dst) and isfile(src) and src.endswith(('.png','.jpg','.pdf')):
    shutil.copy(src, dst_resources)
