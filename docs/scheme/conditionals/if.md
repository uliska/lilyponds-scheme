# `if`

The `if` conditional is the most basic code switch in more or less any
programming language.  In Scheme it has the general form

```
(if test consequent alternative)
```

If the expression `test` evaluates to “a true value” then the subexpression
`consequent` is evaluated, otherwise `alternative`, and the whole `if`
expression evaluates to the value of the chosen subexpression.  OK, let's
clarify this with an example, but first of all we have to understand what “a
true value” means.

### ”True Values”

Scheme knows the literals `#t` for “true” and `#f` for “false”, which are
returned by many comparing expressions and particularly all predicates:

```
guile> (> 2 1)
#t

guile> (string=? "Yes" "No")
#f

guile> (number? 1)
#t

guile> (list? "I'm a list?")
#f
```

However, in Guile Scheme *every object except `#f`* is considered to have “a
true value”.  So the following expressions *all* have “a true value”:

```
"Foo"
'bar
'(1 . 2)
'()
```

That means that whenever the expression `test` evaluates to *anything except
`#f`* then `consequent` is evaluated, otherwise `alternative`.

### Evaluating `if` expressions

So here is the first concrete example

```
guile>
(if (> 2 1)
    "Greater"
    "Smaller")
"Greater"

guile>
(if (> 1 2)
    "Greater"
    "Smaller")
"Smaller"
```

In the first case the test is the expression `(> 2 1)` which evaluates to `#t`
(2 *is* greater than 1), therefore the `consequent` subexpression is evaluated.
In this case it is the self-evaluating string `"Greater"`,  but it could as well
be a complex expression or a symbol referring to a variable.  This string then
becomes the value of the whole `if` expression, and therefore this is printed as
the result.

In the second case the test expression evaluates to `#f`, therefore the whole
expression evaluates to `"Smaller"`.

The most important thing to understand here is that the subexpressions
*evaluate* to a value and don't necessarily *do* anything, and that the same is
true for the whole `if` expression.  This is what I meant with the different
paradigm: in Scheme an `if` expression should be phrased colloquially as
“depending on the result of the test this evaluates to one or the other” instead
of “depending on the test do this or that”. This is best demonstrated in a local
binding (which is also a common use case for conditionals):

```lilypond
#(display
  (let* ((rand (random 100))
         (state (if (even? rand)
                    "even"
                    "odd")))
    (format "The random number ~a is ~a" rand state)))
```

We have a `let*` expression at the core of this example. It establishes two
bindings, first a random integer and then its “state”.  The value bound to the
`state` name is the result of an `if` expression, namely one of the strings
`“even”` or `“odd”`, depending on the result of the application of the `even?`
procedure.  The *body* of the `let*` expression is the invocation of the
`format` procedure which evaluates to a string.  Therefore the value of the
whole `let*` expression is the value of the `format` expression, which is then
passed to the `display` procedure, which prints for example `The random number
61 is odd` to the console.

### Special Cases

#### Unspecified Values

The example discussed above is the default case for `if` expressions, but there
are a number of special cases you should know about - because they can be both
confusing and useful.  The first topic to discuss is the value of the
subexpressions.

Depending on the test one subexpression will be evaluated, and its value becomes
the value of the `if` expression.  However, expressions do not necessarily
evaluate to a value but can also be `<unspecified>`:

```
guile>
(if #t
    (display "true")
    (display "false"))
```

The subexpression `(display "true")` will print something to the console but
doesn't evaluate to anything, and consequently the whole expression *also* has
an unspecified value.

#### No alternative expression

The alternative expression can be omitted in an `if` expression, making it `(if
test consequent)`.  This will work, but when the test fails (i.e. the
alternative expression is requested to be evaluated) the value of the `if`
expression will be unspecified.  This may be acceptable or not, depending on the
context.  For example, if the subexpression is used to *do* something instead of
*returning* a value there's no problem at all.
