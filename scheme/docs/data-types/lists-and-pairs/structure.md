# List Types and Internal Structure

This chapter gives some more in-depth details about how Scheme lists are
constructed, and what implications this has on their use.  Please note that this
is a somewhat advanced topic and you will probably *not* come across it too
early in your learning curve with Scheme in LilyPond.  However, there *are*
occasions where these characteristics can appear at the surface with nastily
confusing situations which can best be handled with a proper understanding of
the underlying structures.

Maybe it is a good idea to have at least a cursory glance at the chapter, just
to know what it is about.  Once you run into a corresponding issue you'll know
where to search for further information.

## How Scheme Lists Are constructed

In the previous chapter we saw that lists are *entered* as a sequence of
elements separated by spaces.  Lists are also *displayed* that way, but this is
not how they are organized internally.

A list in Scheme is a *pair* whose `cdr` is the rest of the list.  The `car` of
this rest is the next list element and its `cdr` the further remainder of the
list. In fact this structure is also known as *linked list*, where the elements
don't know about the list as a whole but are only linked to their subsequent
element.  As a consequence you can say that any list is also a pair but that a
pair is not necessarily a list:

```
guile> (define lst (list 1 2 3 4))
guile> (define pr (cons 5 6))
guile> lst
(1 2 3 4)
guile> p
(5 . 6)
guile> (list? lst)
#t
guile> (list? p)
#f
guile> (pair? lst)
#t
guile> (pair? p)
#t
```

Let's inspect the list `lst` a little closer:

```
guile> (car lst)
1
guile> (cdr lst)
(2 3 4)
```

The `car` of the list is `1` and the `cdr` is the list `(2 3 4)`, the `car` of
that remainder is `2` and the  `cdr` the list `(3 4)`. The `car` of *this*
remainder is `3` and the `cdr` - the list `(4)`.

This last information may be confusing, but on second thought it is quite
natural: The `cdr` of a list element is a list, and so the last element has to
be a list as well.  But what *is* this one-element list?  As we defined earlier
a list is a pair whose `cdr` is a list. So let us inspect this one-element list
individually:

```
guile> (define ll (list 4))
guile> ll
(4)
guile> (car ll)
4
guile> (cdr ll)
()
```

Now we see that the `car` of the last element is the value `4`, while the `cdr`
is an empty list.  This kind of list - where the last element's `cdr` is an
empty list - is called a *proper list* (we'll see improper lists below).  One
consequence of this can be somewhat confusing: whenever you have to retrieve the
last element of a proper list you don't really look for the “last element” but
rather “the car of the last element”.  We will return to this issue in the next
chapter.

#### Constructing Lists As Chained Pairs

If we take our definition literally that a list is a chain of pairs it should be
possible to create a list that way as well:

```
guile> (define pl
  (cons 1
    (cons 2
      (cons 3
        (cons 4 '())))))
guile> pl
(1 2 3 4)
```

What happens here is that we define `pl` to be a pair of `1` and a pair of `2`
and a pair of `3` and a pair of `4` and an empty list.  The same is possible
using the literal notation:

```
guile> '(1 . (2 . (3 . (4 . ()))))
(1 2 3 4)
```

#### Improper Lists

What happens if the last element of a list is *not* a pair with an empty list as
`car` but a simple value?  This is not hypothetical but easily achievable:

```
guile> '(1 . (2 . (3 . 4)))
(1 2 3 . 4)
```

This is Scheme's syntax for an *improper* list, where the last element's `cdr`
is a value instead of a pair.  The dot is an indicator of the last element's
nature as a pair between the `3` and `4` instead of between the `4` and an
invisible trailing element.  Such improper lists can also be created using
`cons` and written as literals:

```
guile> (cons 1 (cons 2 (cons 3 4)))
(1 2 3 . 4)
guile> '(1 2 3 . 4)
(1 2 3 . 4)
```

#### Concatenating Lists

Maybe this section is more about *working* with lists, but we insert it here
because it provides more insight on how lists are structured internally.

The procedure `append` takes a list and appends another list at its end, as can
be seen like this:

```
guile> (define lst (list 1 2 3 4))
guile> lst
(1 2 3 4)
guile> (append lst (list 5 6))
(1 2 3 4 5 6)
```

From the user's perspective we have a list `(1 2 3 4)` and add the elements `5`
and `6` to it.  But we have to understand this from what we have learnt above.
What `append` *really* does is replace the empty list that is the `cdr` of the
first list's last element with the second argument, here `(5 6)`.  So what
originally was `'(4 . ())` has now become `'(4 . (5 . (6 . ())))`.  And as this
seamlessly integrates with the construction of chained pairs the overall result
is a coherent list `(1 2 3 4 5 6)`. Let's see what happens if we don't append a
list but instead a pair:

```
guile> (append lst (cons 5 6))
(1 2 3 4 5 . 6)
```

The result is an improper list, and by now we can easily explain why this is the
case: we have replaced the trailing empty list with a pair whose `cdr` is *not*
a list but instead a plain value.

The same is true if we append a literal value to the list:

```
guile> (append lst 5)
(1 2 3 4 . 5)
```

This time we have directly replaced the `cdr` of the last element with a literal
value, with the same effect of turning the list into an improper list.

Finally we check what happens when we try to append anything to the resulting
improper list:

```
guile> (define lst2 (append lst 5))
guile> lst2
(1 2 3 4 . 5)
guile> (append lst2 6)
standard input:10:1: In procedure append in expression (append l2 6):
standard input:10:1: Wrong type argument in position 1 (expecting empty list): 5
ABORT: (wrong-type-arg)
```

This doesn't work, and also here we are now able to explain why: we said that
`append` replaces the empty list in the last element's `cdr` with the appended
value.  But the improper list does *not* have such a trailing empty list,
instead the `cdr` is `5`, and therefore `append` can't do its work.
