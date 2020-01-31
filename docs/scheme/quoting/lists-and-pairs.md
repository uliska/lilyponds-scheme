# Creating Quoted Lists and Pairs

#### Lists

As we have seen earlier it is not possible to directly write a list object
because Scheme will try to apply the first element as a procedure to the
remaining elements:

```
guile> (1 2 3)
standard input:98:1: In expression (1 2 3):
standard input:98:1: Wrong type to apply: 1
ABORT: (misc-error)
```

Scheme tries to read `1` as a procedure and apply it to `2` and `3`, which
obviously fails. The “wrong type” in the error message refers to `1` being a
number and not a procedure.  The regular syntax to create that list is to use
the `list` procedure in the first place:

```
guile> (list 1 2 3)
(1 2 3)
```

Numbers are self-evaluating, but if we pass symbols to `list` they are evaluated
before being added to the list:

```
guile> (list red green blue)
((1.0 0.0 0.0) (0.0 1.0 0.0) (0.0 0.0 1.0))
```

But what if we want to store the symbols as *names*, that is we want the result
to evaluate to `(red green blue)`?  Of course we can quote the symbols, using
either `quote` or the shorthand notation:

```
guile> (list (quote red) (quote green) (quote blue))
(red green blue)

guile> (list 'red 'green 'blue)
(red green blue)
```

This may become quite unwieldy in practice, therefore Scheme provides a shortcut
and allows the quoting of the expression as a whole:

```
guile> (quote (red green blue))
(red green blue)
```

Please note that the three elements are surrounded by nested parens: `quote`
quotes one single object, and that is the whole list here.  It is also possible
to use the shorthand notation, and this is what you will likely see and use
most:

```
guile> '(red green blue)
(red green blue)
```

Or in LilyPond syntax:

```lilypond
myList = #'(red green blue)
```

#### Pairs

The same is true for pairs.  You can't enter them literally but you have to
either use the `cons` procedure or quote them through `quote` or `'`:

```
guile> (1 . 2)
standard input:82:1: In expression (1 . 2):
standard input:82:1: Wrong number of arguments to 1
ABORT: (wrong-number-of-args)

guile> (cons 1 2)
(1 . 2)

guile> (quote (1 . 2))
(1 . 2)

guile> '(1 . 2)
(1 . 2)
```

*(Please don't ask about the error message in the first example. Obviously this
expression is so fishy that Scheme isn't even able to produce a meaningful
error ...)*

And as with lists and the `list` constructor elements that are not quoted will
be evaluated:

```
guile> (cons red random)
((1.0 0.0 0.0) . #<primitive-procedure random>)

guile> (cons red blue)
((1.0 0.0 0.0) 0.0 0.0 1.0)
```

#### Digression

> But wait a minute, this last one does *not* look like a pair, isn't it?

Well, this is one of these moments where Scheme's syntactical structures can
drive you crazy when you haven't *really* dug into the core.  Although it isn't
the topic of this chapter it seems appropriate to take the opportunity of a
practical recap of what we have seen in the chapter about the [internal
structure](../data-types/lists-and-pairs/structure.html) of lists.

We can properly retrieve the `car` and `cdr` of this expression:

```
guile> (car (cons red blue))
(1.0 0.0 0.0)
guile> (cdr (cons red blue))
(0.0 0.0 1.0)
```

But should that expression not evaluate to something that looks like

```
((1.0 0.0 0.0) . (0.0 0.0 1.0))
```

?

OK, let's dissect it: we have a pair where both the `car` and the `cdr` are
lists. And earlier we have seen a definition of just that: a “pair whose `cdr`
is a list”. This definition describes - a *list*.  So our pair is just a special
case: when the `cdr` of a pair happens to be a list the whole expression becomes
a list as well.  Sounds somewhat strange but obviously doesn't do any harm (if
you don't take countless hours of scratching newbies' heads into account ...).

We can verify that assumption quite easily.  Usually a list is also a pair but a
pair is *not* a list:

```
guile> (pair? '(red blue))
#t

guile> (list? '(red . blue))
#f
```

But here we can see that our pair *is* at the same time a list:

```
guile> (list? (cons red random))
#f
guile> (list? (cons red blue))
#t
```

But there's one more thing to it. If we explicitly create a list from red and
blue it takes yet another form:

```
guile> (list red blue)
((1.0 0.0 0.0) (0.0 0.0 1.0))
```

What is that?  Well, a *proper* list is a list whose last element is a pair with
an empty list as its `cdr`.  Let's see what the `cdr` of our last (second) list element is:

```
guile> (cdr (list red blue))
((0.0 0.0 1.0))
```

So why are we getting *two* nested paren levels? It gets more and more confusing ...
Well, `blue` is a list, so the `cdr` of our initial expression should be a list,
isn't it? And as we have seen earlier the last element in a list is not the
element itself but a *pair* with the element and an empty list as its elements.
So we can check the `car` and the `cdr` of that last expression:

```
guile> (car (cdr (list red blue)))
(0.0 0.0 1.0)
```

So *this* is the “blue” list we'd expect.

```
guile> (cdr (cdr (list red blue)))
()
```

And *this* is the empty list that makes it a “proper list”.

So if we try to wrap that up we can say: `(list red blue)` creates a proper list
with two elements that are both proper lists as well. `(cons red blue)` on the
other hand creates a list whose *first* element is a list (“red”) while “blue”
is represented as three individual elements.

Being confronted with this kind of stuff can be pretty confusing, not only for
the new user.  But everything can be stripped down to some very basic
fundamental concepts, so don't be frightened but try to dissect things one by
one - and ask on the mailing lists for clarifications, and don't hesitate to
keep asking until you have fully understood the case.
