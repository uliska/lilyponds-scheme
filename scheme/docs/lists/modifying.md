# Modifying Lists

The distinction between filtering/searching lists and *modifying* them is
somewhat blurred, for reasons I will discuss more closely in a minute. You may
notice that also the official reference pages about list
[modification](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/List-Modification.html#List-Modification)
and
[searching](https://www.gnu.org/software/guile/docs/docs-1.8/guile-ref/List-Searching.html#List-Searching)
mix entries in a somewhat arbitrary way.

I will not cover all procedures on this page but try to explain the basic
behaviour. But I strongly recommend you visit the two reference pages and
familiarize yourself with what is available.

#### Changing a Single List Element

`list-set!` is the corresponding procedure to `list-ref`: `

```
(list-set! <list> <index> <new-value>)
```

changes the element addressed by the (zero-based) index argument to the new
value. The trailing `!` in the name indicates (by convention) that `list-set!`
actually modifies the list instead of returning a copy.  The expression
evalulates to the new value.

```
guile> (define a '(1 2 3 4 5))
guile> (list-set! a 1 'b)
b
guile> a
(1 b 3 4 5)
```

You can see that if the list is bound to a variable the change is also persistent.

#### Changing the Remainder of a List

With `list-cdr-set!` you can change the n-th `cdr` of a list to something else,
usually another list.

```
guile> (define a '(1 2 3))
guile> (define b '(4 5 6))
guile> (list-cdr-set! a 1 b)
(4 5 6)
guile> a
(1 2 4 5 6)
```

What does happen here exactly? The procedure determines the list element at
position `1`, which is the *second* element, `2`. Then it sets the `cdr` of this
element to the list `b`, effectively appending the second list to the list head
of the first.

The same list could equally have been cosntructed with

```
guile> (append (list-head a 2) b)
(1 2 4 5 6)
```

with the difference that the latter would have returned a *new* list.
