# Accessing Lists

Accessing lists and retrieving their elements is really similar to handling
pairs - which seems quite natural as lists are built from pairs.  In this
chapter we will discuss the basic procedures to access list elements.

#### car/cdr Access

In the previous chapter we have already seen how the `car` and the `cdr` of
lists can be retrieved, and the `cadr` (and friends) shorthands are available for
lists as well:

```
guile> (define l (list 1 2 3 4))
guile> l
(1 2 3 4)
guile> (car l)
1
guile> (cdr l)
(2 3 4)
guile> (cadr l)
2
guile> (cddr l)
(3 4)
guile> (caddr l)
3
guile> (cdddr l)
(4)
guile> (cadddr l)
4
```

Adding `d`s in the `cXXr` procedure name selects increasingly “right” parts of
the list, while using an `a` as the initial letter selects the corresponding
*value* at that position.

One point of specific interest is the *last* element. As explained in the
previous chapter *any* `cdr` variant retrieves a *list* (at least from a
*proper* list), so `(cdddr l)` also returns `(4)`.  In order to retrieve
*values* from a list on always has to use the `a` as the first letter,
equivalent to using “the car of whatever position in the list we are interested
in”.

As a mental exercise think about what the `cdar` of this list would be and why
`(cddddr l)` returns what it returns (if you have read the previous chapter the
second question should be clear).


#### Other Access Options

Scheme and Guile provide much more convenient ways to handle lists and their
elements.  However, I think these should better be discussed after you are
familiar with more basic concepts.  Therefore I have moved the more elaborate
access methods to a [separate chapter](../../lists/index.html).
