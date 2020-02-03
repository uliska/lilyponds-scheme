#!/bin/bash
# build the LilyPond's Scheme book

# building the "parent" book 'introduction' clears the
# subbok build directories, so in all cases this
# has to come first.
for subbook in introduction scheme lilypond internals
do
  cd $subbook
  mkdocs build
  cd ..
done

# Merge the search indexes of the main and the sub books
# So the whole book set can be searched from every page.
merge-mkdocs-search-indexes
