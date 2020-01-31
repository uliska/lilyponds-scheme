# Accessing List Elements

In addition to the basic procedures `car` and `cdr` Scheme provides a number of
higher-level ways to access the different list items individually.

### Number of Elements of a List

Often it is necessary to know the length, respectively the number of elements of
a list.  This is determined by the `length` procedure:

```
guile> (length '(a b c d))
4
```

Note that this expects a *proper list* to work, applying `length` to an improper
list or a pair will result in an error.

### Indexed access

It is possible to access the n-th element of a list using the `list-ref`
procedure, which is passed first the list and then the requested index as
arguments:

```
guile> (list-ref '(a b c d) 3)
d
guile> (list-ref '(a b c d) 4)
standard input:7:1: In procedure list-ref in expression (list-ref (quote #) 4):
standard input:7:1: Argument 2 out of range: 4
ABORT: (out-of-range)
```

There are two things to note about this: The index is “zero-based”, that means
that the fourth list entry will have the index 3. And it will result in an error
when you try to access a non-existent index as in the second example.  The
highest possible index is *one lower than the length of the list*.  So if the
list has four elements as in our example the highest index is *3*.

In order to avoid this kind of error you can make use of the `length` procedure,
once you have learned about conditionals and iteration constructs later in this
book.  As an example that works already now you can use it to access the last
element of a list:

```
guile>(define lst '(1 2 3 4))
guile>lst
(1 2 3 4)
guile>
  (list-ref
    lst
    (- (length lst) 1))
4
```

In this example we calculate the index of the last element by subtracting one
from the length of the list.

### first/second Access

Guile defines a number of convenience accessor methods to retrieve list elements
by their position specified in English words instead of the number:

```
guile> (define lst '(1 2 3 4 5))
guile> (first lst)
1
guile> (second lst)
2
guile> (fifth lst)
5
```

Such procedures are defined for the first ten elements of a list (i.e. `first`
through `tenth`).  Note that “first” here really means the first, so `(first
lst)` is equivalent to `(list-ref lst 0)`.

In addition there is the `last` procedure that always retrieves the last element
of the list, regardless of its index.  As `list-ref` these functions implictly
retrieve the `car` of an element. So unlike accessing elements through the `car`
and `cdr` functions it is not necessary anymore to explicitly unfold the value
using `car`.  But unexpected results may occur when the list is an improper
list. Please investigate the result of the following expressions yourself - if
you have difficulties with that please refer to the explanation about [list
structure](../data-types/lists-and-pairs/structure.html).

```
guile> (last '(1 2 3 4 5))
5
guile> (last '(1 2 3 4 . 5))
4
```

### Accessing Parts of a List

Sometimes it's necessary to retrieve parts of a list, for example all elements
starting with the third or up to the fourth.  For this the procedures
`list-tail` and `list-head` are provided.

```
guile>(define lst '(1 2 3 4 5 6))
(list-tail lst 2)
(3 4 5 6)
```

`list-tail` takes the list and the starting index as arguments. So in this
example the list elements starting with index 2 are retrieved.  Colloquially one
can also say the arguments specifies the number of elements to be skipped.

```
guile>(define lst '(1 2 3 4 5 6))
(list-head lst 2)
(1 2)
```

With `list-head` the index argument specifies the index *to which but not
including* the list elements are retrieved.  However, again this can
colloquially be expressed much clearer as the “number of retrieved elements”.

If an actual sub-list is required the procedures can be stacked/nested:

```
guile> (list-head (list-tail lst 2) 2)
(3 4)
```

First the `list-tail` expression is evaluated, resulting in the list `(3 4 5
6)`, then this is passed to `list-head`.
