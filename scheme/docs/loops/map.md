# Mapping List Elements

#### Single Lists

`map` “maps” the elements of a list to a new list, creating a new list from the
results of the application of a procedure to each element.

```scheme
(map proc list)
```

is the basic form of `map`. `proc` is a procedure accepting a single argument.
The value of `proc` after evaluation will be added to the resulting list. As
with `filter` there are not many applications for the built-in procedures, so
more examples with custom procedures will be given below.

```scheme
guile>(map abs '(-2 4 -0.25 1))
(2 4 0.25 1)
```

`map` takes two arguments here, a *procedure* and a *list*. Note that the
procedure `abs` (determining the “absolute” or positive value of a number) is
passed *without* the parens, as the bare procedure. Now `map` iterates over all
elements of the list, applies `abs` to them and creates a list composed of the
evaluations of `abs`.

Somewhat more involved and interesting is using `car` and friends to dissect
nested and association lists. If you type `all-grob-descriptions` in your Scheme
sandbox you will be faced with the display of a very big nested list. Each list
element is itself a list with the first element being a symbol representing the
grob name and multiple pairs documenting the properties and default values. This
is just the *first* list element describing `Accidental` (already formatted for
better reading):

```scheme
(Accidental
  (after-line-breaking . #<primitive-procedure ly:accidental-interface::remove-tied>)
  (alteration . #<procedure accidental-interface::calc-alteration (grob)>)
   (avoid-slur . inside) (extra-spacing-width -0.2 . 0.0)
   (glyph-name . #<procedure accidental-interface::glyph-name (grob)>)
   (glyph-name-alist
     (0 . accidentals.natural)
     (-1/2 . accidentals.flat)
     (1/2 . accidentals.sharp)
     (1 . accidentals.doublesharp)
     (-1 . accidentals.flatflat)
     (3/4 . accidentals.sharp.slashslash.stemstemstem)
     (1/4 . accidentals.sharp.slashslash.stem)
     (-1/4 . accidentals.mirroredflat)
     (-3/4 . accidentals.mirroredflat.flat))
  (stencil . #<primitive-procedure ly:accidental-interface::print>)
  (horizontal-skylines . #<unpure-pure-container #<primitive-procedure ly:accidental-interface::horizontal-skylines> >)
  (vertical-skylines . #<unpure-pure-container #<primitive-procedure ly:grob::vertical-skylines-from-stencil> #<primitive-procedure ly:grob::pure-simple-vertical-skylines-from-extents> >)
  (X-offset . #<primitive-procedure ly:grob::x-parent-positioning>)
  (Y-extent . #<unpure-pure-container #<primitive-procedure ly:accidental-interface::height> >)
  (meta (name . Accidental)
  (class . Item)
  (interfaces grob-interface accidental-interface font-interface inline-accidental-interface item-interface)))
```

In order to extract a plain listing of all grob *names* we have to retrieve the
first element from each sub-list, which can conveniently be achieved using
`car`.

Entering

```scheme
(map car all-grob-descriptions)
```

in the sandbox will show you a long list with (only) all grob names, which is
very manageable but not that printable here on this page ...

#### Multiple Lists

Interestingly (and different from most other languages) `map`
supports mapping of *multiple* lists.  In fact `map` does *not* accept exactly
one list argument, instead the given procedure must accept as many arguments as
there are additional list arguments. Then it passes the corresponding elements
of all lists to the procedure.

```
guile> (map cons '(1 2 3 4) '(2 3 4 5))
((1 . 2) (2 . 3) (3 . 4) (4 . 5))
```

Each corresponding element of both lists is passed to `cons` as one of its
arguments, so `cons` can combine the corresponding elements of both lists to a
pair.

You should take care of having lists of equal length because extra elements of
the longer list are discarded without any further warning.

```
guile> (map cons '(1 2 3) '(2 3 4 5))
((1 . 2) (2 . 3) (3 . 4))
```

`map` supports procedures with arbitrary numbers of arguments, as long as they
match the number of passed lists:

```
guile> (map list '(1 2 3) '(4 5 6) '(7 8 9))
((1 4 7) (2 5 8) (3 6 9))
```


#### Using `map` to Dissect Nested Lists

Let's complete this section with a slightly complex example making use of a
`lambda` expression to transform a list to a different structure.

Let's define a “context mod” variable:

```lilypond
contextMod = \with {
  instrumentName = "Violin"
  shortInstrumentName = "Vl."
}

mods = #(ly:get-context-mods contextMod)
```

A `\with {}` clause is generally used for modifying contexts, for passing
additional parameters to the creation of voices or staff contexts etc. But it
can also be (ab?)used as a function argument to specify a list of key-value
pairs. In order to make it usable we have to extract the actual content through
`ly:get-context-mods`, which is assigned to the `mods` variable.

```lilypond
#(write mods)
% => ((assign instrumentName "Violin") (assign shortInstrumentName "Vl."))
```

`mods` is now a list with two elements, each of which is a three-element list of
the symbol `assign`, the key name and the value. In order to make use of this as
a configuration store we want to convert it into an [association
list](../alists/index.html), i.e. a list consisting of key-value pairs. We want
each pair to have the second element as its key and the third element as its
value part, so we could - manually - construct it like this:

```lilypond
options =
#(list
  (cons 'instrumentName "Violin")
  (cons 'shortInstrumentName "Vl."))

#(write options)
% => ((instrumentName . Violin) (shortInstrumentName . Vl.))
```

But of course this only works because we know the actual input list, in any
real-world cases we have to resort to a more generic approach: *mapping*.

We need to create a list of pairs where each pair matches an element of our input
list. So we can `map` the list over a procedure that converts each sub-list of
the original input list to the desired pair. As such a procedure does not exist
we will have to write it on our own.

The following `lambda` expression creates a procedure that takes exactly one
argument and evaluates to a pair created from the argument's second and third
element (obviously expecting a list of at least three elements):

```scheme
(lambda (mod)
  (cons (second mod) (third mod)))
```

So this is an expression that *evaluates* to a procedure. That means when using
it with `map` we *do* have to *invoke* the lambda expression, i.e. surround it
with parens. Let's write this in LilyPond again:

```lilypond
options =
#(map
  (lambda (mod)
    (cons (second mod) (third mod)))
  mods)
  #(write options)
  % => ((instrumentName . "Violin") (shortInstrumentName . "Vl."))
```

As this process is something very useful we can now write a function that
directly converts a `\with {}` expression into such a property alist. And in
fact I have done exactly this in openLilyLib, more concretely in
[oll-core](https://github.com/openlilylib/oll-core):

```lilypond
#(define (context-mod->props mod)
   (map
    (lambda (prop)
      (cons (cadr prop) (caddr prop)))
    (ly:get-context-mods mod)))
```

The naming of elements indicates their use here: the input is about *mods* (the
context-mod) while internally the sublists are considered *properties*.
