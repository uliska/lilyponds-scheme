#/usr/bin/env python3

# Script to merge the search index files of the main and all sub books.
# MkDocs generates JSON files with search indexes upon building a site,
# and this doesn't properly work with this project's approach of
# multiple book parts, which only get their *own* index generated
# automatically by MkDocs.
#
# This script updates the JSON index files and adds the indices of the
# other book parts, updating the relative links accordingly.
#
# The script is based on the assumption that subbooks are stored in
# direct subdirectories of the site root. To add more books it should be
# sufficient to add their path names to the BOOKS list.

import json
import os

# Relative path to generated website, from this script
SITE_ROOT = 'site'

# Names of the main books and the book parts
BOOKS = [
    'introduction', # Main book
    'scheme',
    'lilypond',
    'internals'
]

class AbstractBook(object):
    """
    A book part (main or sub), handling the JSON file
    and the relative links to/from the other book parts.
    """
    def __init__(self, root, book_name):
        """Initialize the book object."""
        # Core properties
        self._root = root
        self._book_name = book_name
        # Path components to be set in subclasses
        self._path_from_main = ''
        self._path_from_sub = ''
        # JSON representation of all links pointing into this book part,
        # with the links modified from the main or a sibling book part.
        self._json_from_main = None
        self._json_from_sub = None
        # Path to the JSON file with search index.
        self._json_file = os.path.join(
            root,
            SITE_ROOT,
            book_name,
            'search',
            'search_index.json'
        )
        # Read original search index
        with open(self.search_index_file(), 'r') as f:
            self._original = f.read()
        # Store plain text (modified links are created from here)
        self._original_json = json.loads(self._original)
        # Original search index as generated by MkDocs
        self._original_json = None

    def json(self):
        """Return (and cache) JSON representation of search index."""
        if not self._original_json:
            self._original_json = json.loads(self._original)
        return self._original_json

    def json_docs(self, member, path):
        """
        Return (and cache) the "docs" element of the search index,
        with updated links pointing to this book from the main book
        or another subbook.
        The relative paths used for this are stored in the subclasses.
        """
        if not member:
            full_json = json.loads(
                self.replace_location(path)
            )
            member = full_json['docs']
        return member

    def json_from_main(self):
        """Return the docs with links to this from the main book."""
        return self.json_docs(self._json_from_main, self._path_from_main)

    def json_from_sub(self):
        """Return the docs with links to this from a sibling subbook."""
        return self.json_docs(self._json_from_sub, self._path_from_sub)

    def replace_location(self, path):
        """Return a copy of the original index string, with all relative
        paths updated according to the given path."""
        return self._original.replace(
            '"location":"',
            '"location":"{}'.format(path)
        )

    def search_index_file(self):
        """Return absolute path of JSON search index file."""
        return self._json_file

    def update_json(self, sub_books, main_book=None):
        """Update the JSON file with the additional indices.
        The concrete implementation is done in the subclasses."""
        self._update_json(sub_books, main_book)
        with open(self.search_index_file(), 'w') as f:
            f.write(json.dumps(self.json()))


class MainBook(AbstractBook):
    """The main book which includes the subbooks."""

    def __init__(self, root, book_name):
        super(MainBook, self).__init__(root, '')
        # Path from main to main is actually unused.
        self._path_from_main = ''
        self._path_from_sub = '../'

    def _update_json(self, sub_books, main_book=None):
        """Extend index with indexes from the main book to all subbooks."""
        docs = self.json()['docs']
        for b in sub_books:
            docs.extend(b.json_from_main())


class SubBook(AbstractBook):
    """A book part/subbook."""

    def __init__(self, root, book_name):
        super(SubBook, self).__init__(root, book_name)
        self._path_from_main = '{}/'.format(book_name)
        self._path_from_sub = '../{}/'.format(book_name)

    def _update_json(self, sub_books, main_book):
        """Extend index with indexes to the main book and the other subbooks."""
        docs = self.json()['docs']
        docs.extend(main_book.json_from_sub())
        for b in sub_books:
            if not b == self:
                docs.extend(b.json_from_sub())


class Main(object):
    """A class instead of a main() function"""
    def __init__(self, book_names):
        # We assume the script is called from within the repository
        self._root = os.path.dirname(os.path.realpath(__file__))
        self._main_book = None
        self._sub_books = []
        self.init_books(book_names)
        self.update_books()

    def init_books(self, book_names):
        """Create the book objects, load indexes from disk."""
        self._main_book = MainBook(self._root, book_names[0])
        for name in book_names[1:]:
            self._sub_books.append(SubBook(self._root, name))

    def update_books(self):
        """Update the JSON indexes for all books and save to disk."""
        self._main_book.update_json(self._sub_books)
        for b in self._sub_books:
            b.update_json(self._sub_books, self._main_book)


def warn():
    print("Script to merge the search indexes of the books")
    for b in BOOKS:
        print('- {}'.format(b))
    print()
    print('NOTE:')
    print('This script should only be called *after* all book parts')
    print('have been created. Otherwise file access errors may occur.')

warn()
Main(BOOKS)
