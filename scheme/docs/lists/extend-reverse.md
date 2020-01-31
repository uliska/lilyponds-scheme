# Extending and Reversing Lists

The title of this section is a little bit misleading as the discussed procedures
do not actually *modify* the lists but return a modified *copy* of the original
list(s).  However, they are nevertheless very useful in common programming
tasks.

## Appending Lists to Lists

`append` takes (at least) two lists and returns a new list that concatenates
them:

```
guile>(define a '(1 2 3))
guile>(define b '(4 5 6))
guile>(define c '(a b c))
guile>(append a c b)
(1 2 3 a b c 4 5 6)
```

Note that the lists defined as `a`, `b` and `c` are not changed through these
operations. In order to make use of the resulting list you will have to bind it
to something else:

```
guile>(define c (append a b))
guile>c
(1 2 3 4 5 6)
```

### Appending a Single Element to a List

Of course it is possible to append single elements to a list, and in fact this
is a very common task. However, there is a caveat that can lead to a very
typical error:

```
guile> (append '(1 2 3) 4)
(1 2 3 . 4)
```

Appending a single element seems to create an *improper list!* But if we take a
step back and consider what actually happens when lists are concatenated it is
clearly correct behaviour.

We know that lists in Scheme are chained pairs, with the `car` of each pair
holding the data of the element and the `cdr` pointing to the next element's
pair. The last element of a proper list is also a pair, with the `cdr` being the
*empty list* `()`. What `append` actually does is pointing that trailing empty
list to the appended list, making the first element of the second list a natural
member of the first. Consequently, when we append the simple value `4` to a list
the `cdr` of the last list element *becomes* `4` - making the first list an
improper list.

Fortunately the “solution” is very easy - just something one tends to forget
most of the time.  “`append` takes (at least) two lists” is what I wrote at the
top, and you have to take that literally: you need a *list*, even if it consists
of only one element. So the proper way would have been to write

```
guile>(append '(1 2 3) '(4))
(1 2 3 4)
```

**NOTE:** As an exercise you can figure out how to achieve that result by not
appending a *list* but a *pair*.

## Reversing Lists

As with the above `reverse` does not change the list itself but returns a new
list with the same elements in reverse order. The behaviour is not surprising at
all:

```
guile>(reverse '(1 2 3 4))
(4 3 2 1)
```

Apart from simply reverting the order of a complete list `reverse` can be made
useful for accessing list elements from the end. For example the second-to-last
element of a list with unknown length can be accessed through `(second (reverse
'(1 2 3 4)))` (which would evaluate to `3`). The same result could be achieved
using `(list-ref '(1 2 3 4 ) (- (length '(1 2 3 4)) 2))`, but apart from needing
to refer to the list *twice* this may be semantically less straightforward, and
often you'd prefer juggling with reversed lists. As another example you can
retrieve all the elements of a list *except the last* through

```
guile> (reverse (cdr (reverse '(1 2 3 4))))
(1 2 3)
```

First we reverse the list, then we apply `cdr` (giving us all elements except
the first one (i.e. the last one of the original list)), and finally we reverse
the order again.  As an exercise you should try achieving the same result using
`list-head`.
