# Searching and Filtering Lists

Often it is necessary to choose elements from list based on certain criteria, or
in other words: to search and filter lists.  As lists are the core of Scheme as
a LISP language there are of course readily available tools for that purpose.

## Searching for Elements in a List

To determine if an element is present in a list Scheme provides the triple

* `memq`
* `memv`
* `member`

each representing one of the three [equality](../equality.html) modes.  The functions are called as

```
(<function> <element> <list>)
e.g.
(memv 3 '(1 2 3 4 5))
```

Colloquially you could translate this into “check if `3` is a member of the list
`'(1 2 3 4 5)`” - which it is -, but actually the function works somewhat
differently.  From the introduction to [data types](../data-types.index.html)
you may recall that for that type of question one uses *predicates*, procedures
that return `#t` or `#f` according to the result of some test. But predicate
names by convention have a trailing question mark, which `memq`, `memv` and
`member` do not have. This is not an inconsistency but rather indicates that the
function does *not* return `#t` or `#f`. Instead it returns *the remainder of
the list, starting with the first matched element, or `#f` if the element is not
found in the list*.  The result of the above example would therefore be the list
`(3 4 5)`.

The fact that `member` and friends return either `#f` or a “true value” can be
exploited to create elegant solutions in
[conditionals](../conditionals/index.html).

## Filtering Lists

Sometimes it is necessary to produce a list resulting of all elements in a given
list that match (or do not match) given criteria. This can be achieved through
applying `filter` or `delete` to a list

#### filter

```
(filter <predicate> <list>)
```

`filter` applies `<predicate>` to each element of `<list>` and creates a new
list consisting of each element satisfying the predicate.  `<predicate>` can be
any procedure taking exactly one argument and returning a value. The predicate
is “satisfied” whenever it returns a “true” value, that is anything except `#f`.

I will make this clearer through an example.  The easiest case is applying a
type predicate, keeping all elements that match a certain type:

```
guile> (filter number? '(1 2 "d" 'e 4 '(2 . 3) 5))
(1 2 4 5)
```

In this case `filter` applies the predicate `number?` to each element of the
list `'(1 2 "d" 'e 4 '(2 . 3) 5)` and constructs the resulting list from all
numbers in this list.  Note that the pair `'(2 . 3)` is *not* a number although
it consists of only numbers.

In this basic form `filter` is somewhat limited because it can only be used with
procedures accepting a single argument, i.e. “predicates”.  Although there are
other procedures that match this requirement it is rarely useful to use them in
a `filter` expression.  When interested in things like “all list elements that
are numbers greater than 7” or “all list elements are pairs of numbers where the
`cdr` is greater than the `cdr`” you will want to use custom procedures, which
you'll learn to write in [Defining Procedures](../scheme/procedures/index.html).

#### delete and delete-duplicates

`delete` is somewhat like the opposite of `filter` in so far as it returns a
copy of a list with all elements that *do not* match the given criteria. The
difference is that the match is not determined through a *predicate* but by
comparing the elements with `equal?`.

```
guile>(delete 3 '(1 2 3 4 5 4 3 2))
(1 2 4 5 4 2)
```

The resulting list is the original list with all elements deleted that are
“equal” to `3`.

`delete` has its companion procedures `delq` and `delv` which use `eq?` and
`eqv?` as comparison predicate.

A related procedure is `delete-duplicates`, which returns a copy of the original
list, stripped off any duplicate elements.  The comparison is performed using
`equal?`, so for example strings with the same content are deleted as well:

```
guile> (delete-duplicates '("a" 2 3 "a" b 3))
("a" 2 3 b)
```
