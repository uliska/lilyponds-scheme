# Unquoting

OK, we have seen the quoted and the explicit syntax to create lists and pairs,
the difference being that in the `list` approach the elements are evaluated:

```
guile> '(red random 1)
(red random 1)

(list red random 1)
((1.0 0.0 0.0) #<primitive-procedure random> 1)
```

But quite often one needs a list where *some* elements are taken literally while
others should be evaluated.  Consider the previous example and imagine that with
`random` we don't want to refer to the procedure of that name, but instead read
it as, say, an option name, e.g. one out of a list of `'random`, `'sorted` and
`'weighted`.

The most straightforward approach would be to create the list using `list` and
individually quote the element that needs it:

```
guile> (list red (quote random) 1)
((1.0 0.0 0.0) random 1)
guile> (list red 'random 1)
((1.0 0.0 0.0) random 1)
```

But Scheme offers an alternative approach for this that you will encounter quite
often:

## Quasiquoting

In addition to `quote` Scheme has the procedure `quasiquote`.  On first sight it
does the same as `quote`, namely it quotes an object.  As with `quote` there is
also a shorthand notation available that is usually used in input files, the
backtick <code>&#96;</code>.

```
guile> (quasiquote (red random 1))
(red random 1)

guile> `(red random 1)
(red random 1)
```

So here the list elements are quoted as well.  The difference is that with
`quasiquote` it is possible to *unquote* individual elements within the object.

## Unquoting

*Unquoting* an element, that is, forcing this specific element to be evaluated,
is achieved using `unquote` or its shorthand notation, the comma:

```
guile> (quasiquote ((unquote red) random 1))
((1.0 0.0 0.0) random 1)

guile> `(,red random 1)
((1.0 0.0 0.0) random 1)
```

In this example we have (quasi)quoted the expression as a whole but explicitly
unquoted the `red` element.  You can see that `red` is evaluated while `random`
is read as a name.  

Note that I have used the written and shorthand notations consistently within
each expression, but that is *not* necessary, the shorthand forms can freely be
mixed with the verbal ones, like e.g. `(quasiquote (,red random 1))`.

## Unquoting a List

When unquoting an element that happens to be a list this list is inserted into
the surrounding list as a single item, such as

```
guile> `(1 2 ,(list 3 4) 5)
(1 2 (3 4) 5)
```

However, there are many occasions where you will want the individual items of
that list to be inserted in the resulting list.  This can be achieved with the
`unquote-splicing` syntax or its shorthand “comma-at” `,@`:

```
guile> `(1 2 ,@(list 3 4) 5)
(1 2 3 4 5)
```

To be more concrete, in a quasiquoted expression `unquote-splicing` takes any
Scheme expression that evaluates to a list and inserts the elements individually
in the surrounding list.

## Nesting `quasiquote` Levels

It is possible to nest multiple levels of quoting and unquoting, but we won't
discuss this in more detail as it is not regularly used in LilyPond. But you may
want to keep that fact in mind, in case you encounter a complicated quoted
expression and unquoting doesn't seem to do its job.
