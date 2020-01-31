# Local Binding with `let`

The basic form for local bindings is `let`, which we'll explore in most detail.
The companion procedures `let*` and `letrec` can then be shown quite concisely.
As an example we'll implement a color damper that damps the RGB components of a
color by a given factor. In order to benefit from color highlighting and easier
editing we will do that in LilyPond files and not on the Scheme REPL.

The typical use case for `let` expressions is within procedures where we would
get the original data from the procedure arguments.  But for the sake of our
example we simply create a global variable that we can then reference:

```lilypond
% Create a pair with a color and a damping factor
#(define props (cons yellow 1.3))
```

`props` is now `((1.0 1.0 0.0) . 1.3)`, a pair with a list for the yellow color
and a number for the damping factor.  What we need to do with it is pretty
simple: just create a new list with three elements where each element is the
corresponding element from the `car` of `props` divided by the factor stored in
the `cdr` of `props`.  In order to later display the value (and to practice) we
bind the resulting list to a top-level variable defined in LilyPond syntax:

```lilypond
dampedYellow =
#(list
  (/ (first (car props)) (cdr props))
  (/ (second (car props)) (cdr props))
  (/ (third (car props)) (cdr props)))

#(display dampedYellow)
```

which will print `(0.769230769230769 0.769230769230769 0.0)` to the console.
(You could also use that variable to override a `color` property of a grob, by
the way.)

So what's the problem with that?  It's the redundancy of the calls to `car` and
`cdr`, three times for each.  Each time we need the color or the damping factor
we have to access the original variable and extract the data from it.  In the
case of `car` and `cdr` this is not a real issue but in real-world code one will
have expressions that are considerably more complicated to write *and*
computationally more expensive.

The solution is to create local bindings of the values of `(car props)` and
`(cdr props)` and then refer to these bindings within the body of the
expression.  This is done with the `let` expression that takes the general form

```
(let (<bindings>) exp1 exp2 ...)
```

or, displayed in a more hierarchical manner:

```
(let
  (
    <binding 1>
    <binding 2>
    ...
  )
  <expression 1>
  <expression 2>
  ...
)
```

The `let` expression has two parts, the *bindings* and the *body*, where each
part must have *at least* one entry.  The bindings are enclosed by parens as a
whole, and each binding has the form `(name value)` where `name` is a symbol
(the “name” of the local binding) and `value` any Scheme value.  While the value
could be of any type including literal values the whole point of it is to bind
the results of complex expressions to simple names.

In our example we create two bindings, one for the color and one for the damping
factors, which looks like this:

```
(let
  (
    (color (car props))
    (damping (cdr props))
  )
  <expression 1>
  <expression 2>
  ...
)
```

Now we have two “local variables”, `color` and `damping` that are visible and
accessible from within the *body* of the `let` expression.

This body of a `let` expression is an arbitrary number of expressions that is
evaluated in sequence.  Note that - different from the bindings - there is *no*
extra layer of parens around the body.  The value of the *final* expression will
become the value of the `let` expression as a whole.  In our example we only
have *one* expression, the `list` creation.  But instead of repeatedly calling
`car` and `cdr` we can now use the local variables directly.

As this `list` expression is the only (and therefore last) in the body the whole
`let` expression evaluates to the created list, and this value (with the damped
color) is bound to the top-level variable:

```lilypond
dampedYellowWithLet =
#(let
    (
      (color (car props))
      (damping (cdr props))
    )
    (list
      (/ (first color) damping)
      (/ (second color) damping)
      (/ (third color) damping)
    )
 )

#(display dampedYellowWithLet)
```

which will print the same result as before.

The indentation of the previous example was pretty unidiomatic and intended to
exemplify how we constructed the expression step by step.  Usually one would use
a more condensed way, for example

```lilypond
dampedYellowWithLet =
#(let ((color (car props))
       (damping (cdr props)))
   (list
    (/ (first color) damping)
    (/ (second color) damping)
    (/ (third color) damping)))
```

You may think that this expression is considerably more complex than our
initial, direct application of `list`.  But as mentioned the `car` and `cdr`
expressions are comparably simple, and the “complexity ratio” will change
dramatically with more complex expressions.

The nesting and parenthesizing levels in that code look daunting, but indeed
they are the result of a completely consequent structure, and (in theory)
there's no room for misunderstandings.  However, the frustrating truth is that
in practice (for the beginner) it *is* a miracle how and where to place the
parens, and the error messages aren't really encouraging, to say the least.
Therefore I have written a dedicated chapter discussing the typical error
conditions we tend to produce.
