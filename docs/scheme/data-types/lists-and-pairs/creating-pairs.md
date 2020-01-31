# Creating Pairs

The basic unit of compound data types in Scheme is the *pair*, an item with two
values.  Pairs are used very often as properties for graphical score items in
LilyPond, so everybody should be familiar with seeing and entering them:

```lilypond
{
  \override Beam.positions = #'(2 . 5)
  \once \override DynamicText.extra-offset = #'(-2 . 4)
  c'8 \p b a b
}
```

{% image
   caption="Pairs as overrides",
   href="assets/images/pairs-fullsize.png" %}
  /assets/images/pairs-small.png
{% endimage %}

## Writing Pairs as Literals

In this example the `positions` property of the beam and the `extra-offset` of
the dynamics have been deliberately changed using pairs. In Scheme a pair as a
literal value is written as two arbitrary values, enclosed in parens and
separated by a dot.  The parens are prepended with the `'` single quote, and in
order to tell the parser to interpret the following as Scheme the whole
expression is prepended with the `#` hash. When entering pairs like this - as
literal values - there are a few things one should be really clear about.

Pairs are not limited to numbers - as in the previous example - but can hold
*any* type of data.  It doesn't matter whether there is whitespace between the
parens and the values, but it is important that the separating dot is surrounded
by whitespace because otherwise the results will be unexpected:

```
guile> '(2 . 3.2)
(2 . 3.2)

guile> '(red . "hello")
(red . "hello")
```

The first example is a pair consisting of an integer and a real number, the
second of a symbol and a string.  This is something one could stumble over: a
[few chapters earlier](../symbols.html) we have seen that `red` in LilyPond
refers to a variable of type `color?` and evaluates to a list with three
elements.  So shouldn't that somehow be reflected here as well?

The secret lies in the leading single quote `'`. This “quotes” the following
expression and prevents Scheme from evaluating the enclosed elements, instead
they are taken literally. We have touched this already when discussing
[symbols](../symbols.html) but we will cover the concept of
[quoting](../../quoting.html) in depth in a dedicated chapter.

```
guile> '( 1 . 3/4     )
(1 . 3/4)

guile> '(apple .2)
(apple 0.2)

guile> '(1. 3)
(1.0 3)

guile> '(red. 4)
(red. 4)
```

The first of these examples shows that spaces between the parens and the values
are silently ignored. But the other three examples produce unexpected results in
so far as when the whitespace around the dot is missing this is interpreted as
belonging to one of the values. `.2` is implicitly completed to `0.2`, `1.` to
`1.0` (thus converting an integer to a real number), and in case of the symbol
the dot simply becomes part of that symbol `red.`.  It is important to note that
there is no additional dot left in the resulting expression: Scheme has created
a *list* now instead of a *pair*. We leave this distinction for now and will get
back to it in the next chapter.

## Explicitly Creating Pairs

Directly writing literal pairs is not the only way to create them, in fact it is
a shorthand that can be used instead of the “proper” way.  Instead pairs can
also be created using the procedure `cons`:

```
guile> (cons 1 3/4)
(1 . 3/4)

guile> (cons "Hi" 2.0)
("Hi" . 2.0)

guile> (cons red 5)
((1.0 0.0 0.0) . 5)

guile> (cons 1 2 3)
ERROR: Wrong number of arguments to #<primitive-procedure cons>
ABORT: (wrong-number-of-args)
```

`cons` is a procedure that is applied to two elements and evaluates to the pair
consisting of these two elements.  It is an error to provide a different number
of elements than two, as can be seen in the last example.

Now when looking at the third example you can see that *this* time `red` is
actually evaluated and the first element of the pair is the list we already know
as the value of `red`.  When creating a pair using `cons` the elements can
really have arbitrary types.  You can even call procedures, as in the following
example that calls the procedure `random` returning a psudo-random real number:

```
guile> (cons (random 10.0) 4)
(5.2 . 4)
```

Here we use the expression `(random 10.0)` that applies the `random` procedure
to the value `10.0`, in this case returning the random number `5.2`.

```
guile> (cons random 10.0)
(#<primitive-procedure random> . 10.0)
```

This time we passed the “naked” `random` procedure to `cons`.  It is *not*
invoked but rather stored in the pair as a procedure.  Admittedly this is
already a somewhat advanced usage but can come in pretty handy, and we want to
present examples of the different ways pairs can handle literals, procedures and
evaluated procedure applications.  Hoping it will help with providing the whole
picture we will close this off with a final example:

```
guile> (cons 'random 10.0)
(random . 10.0)
```

As we have seen earlier it is possible to “quote” symbols to prevent their
evaluation to something extranous (a procedure in this case), so here we used
`random` as a *symbol* to store it in the first element of the pair.

## Closing Thoughts

This chapter started with a familiar example of *pair* usage in LilyPond,
followed by a dissection of how pairs can be created in Scheme.  Having read
through to here you should by now be aware that the overrides from the example
expect "a pair", but not necessarily this familiar way of writing them.  In fact
you can supply *anything* that properly evaluates to a pair of numbers, even
procedures that calculate the overrides on-the-fly.  To show that this is true
we close this chapter with an example where both the beam positions and the
extra-offset of the dynamics is determined by the `random` procedure. *(It has
to be noted that this is only pseudo random and will look identical for every
subsequent compilation.)*

```lilypond
{
  \override Beam.positions = #(cons (random 5.0) (random 5.0))
  \once \override DynamicText.extra-offset = #(cons (random 5.0) (random 5.0))
  c'8 \p b a b
}
```

{% image
   caption="Random pairs as overrides",
   href="assets/images/pairs-random-fullsize.png" %}
  /assets/images/pairs-random-small.png
{% endimage %}
